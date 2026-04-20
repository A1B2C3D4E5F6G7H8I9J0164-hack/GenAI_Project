"""
Load all training CSVs, compute per-file time series (correct lags), cache merged result.
"""

from __future__ import annotations

import glob
import json
import os
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd


def _backend_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def data_dir() -> str:
    return os.path.join(_backend_dir(), "data")


def cache_dir() -> str:
    p = os.path.join(_backend_dir(), "cache")
    os.makedirs(p, exist_ok=True)
    return p


def list_csv_files() -> List[str]:
    paths = sorted(glob.glob(os.path.join(data_dir(), "*.csv")))
    return [p for p in paths if os.path.isfile(p)]


def _file_manifest(paths: List[str]) -> Dict[str, Any]:
    manifest = {}
    for p in paths:
        try:
            manifest[os.path.basename(p)] = os.path.getmtime(p)
        except OSError:
            manifest[os.path.basename(p)] = None
    return manifest


def _manifest_path() -> str:
    return os.path.join(cache_dir(), "dataset_manifest.json")


def _cached_frame_path() -> str:
    return os.path.join(cache_dir(), "engineered_training_df.joblib")


def _load_manifest() -> Optional[Dict[str, Any]]:
    mp = _manifest_path()
    if not os.path.isfile(mp):
        return None
    with open(mp, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_manifest(files_manifest: Dict[str, Any], n_rows: int) -> None:
    payload = {"files": files_manifest, "n_rows": n_rows}
    with open(_manifest_path(), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def _cache_valid(paths: List[str]) -> bool:
    if not paths:
        return False
    if not os.path.isfile(_cached_frame_path()):
        return False
    current = _file_manifest(paths)
    old = _load_manifest()
    if not old or "files" not in old:
        return False
    return old["files"] == current


def _read_one_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["_source_file"] = os.path.basename(path)
    if "Datetime" not in df.columns and "Date" in df.columns and "Time" in df.columns:
        df["Datetime"] = pd.to_datetime(
            df["Date"].astype(str) + " " + df["Time"].astype(str),
            format="mixed",
            errors="coerce",
        )
    elif "Datetime" in df.columns:
        df["Datetime"] = pd.to_datetime(df["Datetime"], format="mixed", errors="coerce")
    else:
        raise ValueError(f"No Datetime/Date+Time in {path}")
    df = df.dropna(subset=["Datetime"])
    return df


def resolve_target_column(df: pd.DataFrame) -> str:
    candidates = [
        "EV Charging Demand (kW)",
        "Charging Demand (kW)",
        "Demand",
        "Adjusted Charging Demand (kW)",
    ]
    for c in candidates:
        if c in df.columns:
            return c
    num = df.select_dtypes(include=[np.number]).columns
    if len(num) == 0:
        raise ValueError("No numeric target column found.")
    return num[0]


def engineer_features_for_station(df: pd.DataFrame, target_col: str) -> pd.DataFrame:
    """Expects single-station dataframe sorted by time."""
    from .feature_columns import add_cyclical_time_features, EXTRA_NUMERIC_FEATURES

    df = df.sort_values("Datetime").reset_index(drop=True)
    df["Hour"] = df["Datetime"].dt.hour
    df["DayOfWeek"] = df["Datetime"].dt.dayofweek

    t = pd.to_numeric(df[target_col], errors="coerce")
    df[target_col] = t
    df = df.dropna(subset=[target_col])

    df["Demand_Lag_1"] = df[target_col].shift(1)
    df["Demand_Lag_2"] = df[target_col].shift(2)
    df["Demand_Lag_3"] = df[target_col].shift(3)
    df["Rolling_Avg_3h"] = df[target_col].rolling(window=3, min_periods=1).mean().shift(1)
    df["Rolling_Avg_6h"] = df[target_col].rolling(window=6, min_periods=1).mean().shift(1)
    df["Rolling_Std_3h"] = df[target_col].rolling(window=3, min_periods=1).std().shift(1)

    defaults = {
        "Electricity Price ($/kWh)": 0.12,
        "Grid Stability Index": 1.0,
        "Number of EVs Charging": 5,
    }
    for col, val in defaults.items():
        if col not in df.columns:
            df[col] = val
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(val)

    for col in EXTRA_NUMERIC_FEATURES:
        if col not in df.columns:
            df[col] = 0.0
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    df["Price_Hour_Interact"] = df["Electricity Price ($/kWh)"] * df["Hour"]
    df["Price_EV_Interact"] = df["Electricity Price ($/kWh)"] * df["Number of EVs Charging"]

    add_cyclical_time_features(df)
    df = df.dropna().reset_index(drop=True)
    return df


def build_merged_engineered_frame(force_refresh: bool = False) -> pd.DataFrame:
    """
    Merge all CSVs under data/, engineering lags within each station file.
    Cached on disk when source mtimes are unchanged.
    """
    paths = list_csv_files()
    if not paths:
        # No CSV data available — generate synthetic training data
        print(f"[dataset] No CSV files in {data_dir()}. Generating synthetic data...")
        try:
            from .generate_synthetic import generate_synthetic_csv
            generate_synthetic_csv(data_dir())
            paths = list_csv_files()
        except Exception as gen_err:
            print(f"[dataset] Synthetic generation failed: {gen_err}")

        if not paths:
            raise FileNotFoundError(
                f"No CSV files found in {data_dir()} and synthetic generation failed."
            )

    if not force_refresh and _cache_valid(paths):
        return joblib.load(_cached_frame_path())

    frames = []
    for path in paths:
        raw = _read_one_csv(path)
        target_col = resolve_target_column(raw)
        part = engineer_features_for_station(raw, target_col)
        part["_target_name"] = target_col
        frames.append(part)

    merged = pd.concat(frames, axis=0, ignore_index=True)
    merged = merged.sort_values("Datetime").reset_index(drop=True)

    joblib.dump(merged, _cached_frame_path())
    _save_manifest(_file_manifest(paths), len(merged))
    return merged


def get_xy(
    columns: List[str],
    target_col: str = "EV Charging Demand (kW)",
) -> Tuple[pd.DataFrame, np.ndarray]:
    df = build_merged_engineered_frame()
    if target_col not in df.columns:
        target_col = resolve_target_column(df)
    y = df[target_col].astype(float).values
    X = df[columns].astype(float)
    return X, y
