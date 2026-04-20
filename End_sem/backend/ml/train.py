"""
Train ensemble regressor on cached engineered data from all CSVs under data/.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler

from .dataset import build_merged_engineered_frame, resolve_target_column
from .feature_columns import full_feature_list


class WeightedEnsemble:
    """Average predictions from several sklearn-compatible regressors."""

    def __init__(self, models: List[Any], weights: List[float]):
        if len(models) != len(weights):
            raise ValueError("models and weights length mismatch")
        self.models = models
        self.weights = np.asarray(weights, dtype=np.float64)
        self.weights /= self.weights.sum()

    def predict(self, X: np.ndarray) -> np.ndarray:
        preds = np.column_stack([m.predict(X) for m in self.models])
        return preds @ self.weights

    def get_params(self, deep: bool = True):
        return {"models": self.models, "weights": self.weights.tolist()}


def _model_paths(base_dir: str) -> Dict[str, str]:
    mdir = os.path.join(base_dir, "models")
    os.makedirs(mdir, exist_ok=True)
    return {
        "bundle": os.path.join(mdir, "model_bundle.joblib"),
        "legacy_model": os.path.join(mdir, "ev_demand_timeseries.pkl"),
        "legacy_scaler": os.path.join(mdir, "scaler.pkl"),
    }


def train_and_save_bundle(base_dir: str, force_refresh_data: bool = False) -> Dict[str, Any]:
    columns = full_feature_list(True)
    df = build_merged_engineered_frame(force_refresh=force_refresh_data)

    target_col = "EV Charging Demand (kW)"
    if target_col not in df.columns:
        target_col = resolve_target_column(df)

    y = df[target_col].astype(float).values
    X = df[columns].astype(float)

    n = len(X)
    split = max(int(n * 0.8), min(500, n // 2))
    X_train_df, X_test_df = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y[:split], y[split:]

    # Holdout metrics (time-ordered; may be pessimistic if regimes shift)
    scaler_eval = StandardScaler()
    X_tr_e = scaler_eval.fit_transform(X_train_df)
    X_te_e = scaler_eval.transform(X_test_df)

    hgb_e = HistGradientBoostingRegressor(
        max_iter=75,
        max_depth=8,
        learning_rate=0.1,
        l2_regularization=0.12,
        min_samples_leaf=20,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=10,
        random_state=42,
    )
    hgb_e.fit(X_tr_e, y_train)
    gbr_e = GradientBoostingRegressor(
        n_estimators=50,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.85,
        max_features="sqrt",
        random_state=42,
    )
    gbr_e.fit(X_tr_e, y_train)
    ens_e = WeightedEnsemble([hgb_e, gbr_e], weights=[0.52, 0.48])
    y_te_hat = ens_e.predict(X_te_e)

    metrics = {
        "holdout_r2": float(r2_score(y_test, y_te_hat)),
        "holdout_mae": float(mean_absolute_error(y_test, y_te_hat)),
        "n_holdout": int(len(y_test)),
        "n_rows": int(n),
        "n_features": len(columns),
    }
    print(
        f"[train] rows={n} holdout={metrics['n_holdout']} "
        f"holdout_R2={metrics['holdout_r2']:.4f} holdout_MAE={metrics['holdout_mae']:.6f}"
    )

    # Production fit: scaler + ensemble on all rows (maximizes accuracy on deployed model)
    scaler = StandardScaler()
    X_all_s = scaler.fit_transform(X)

    hgb = HistGradientBoostingRegressor(
        max_iter=100,
        max_depth=10,
        learning_rate=0.08,
        l2_regularization=0.1,
        min_samples_leaf=12,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=15,
        random_state=42,
    )
    hgb.fit(X_all_s, y)

    gbr = GradientBoostingRegressor(
        n_estimators=75,
        max_depth=6,
        learning_rate=0.08,
        subsample=0.88,
        max_features="sqrt",
        random_state=42,
    )
    gbr.fit(X_all_s, y)

    ensemble = WeightedEnsemble([hgb, gbr], weights=[0.60, 0.40])

    y_all_hat = ensemble.predict(X_all_s)
    metrics["full_fit_r2"] = float(r2_score(y, y_all_hat))
    metrics["full_fit_mae"] = float(mean_absolute_error(y, y_all_hat))

    defaults: Dict[str, float] = {}
    med = X.median()
    for c in columns:
        defaults[c] = float(med[c]) if c in med and np.isfinite(med[c]) else 0.0

    bundle = {
        "estimator": ensemble,
        "scaler": scaler,
        "feature_columns": columns,
        "defaults": defaults,
        "metrics": metrics,
        "target_column": target_col,
    }

    paths = _model_paths(base_dir)
    joblib.dump(bundle, paths["bundle"])

    # Remove legacy artifacts so load_model does not pick stale pickles
    for key in ("legacy_model", "legacy_scaler"):
        p = paths[key]
        if os.path.isfile(p):
            try:
                os.remove(p)
            except OSError:
                pass

    try:
        import importlib

        pred = importlib.import_module("ml.predictor")
        pred._bundle = None
    except Exception:
        pass

    _print_training_report(metrics)
    return bundle


def _print_training_report(metrics: Dict[str, Any]) -> None:
    """Readable console summary after model bundle is written."""
    m = metrics
    line = lambda a, b: f"  │ {str(a).ljust(22)} {str(b).rjust(26)} │"
    print("")
    print("  ╔══════════════════════════════════════════════════════════╗")
    print("  ║           Voltgent — model bundle saved                  ║")
    print("  ╠══════════════════════════════════════════════════════════╣")
    print(line("Rows (train matrix)", m.get("n_rows", "—")))
    print(line("Features", m.get("n_features", "—")))
    print(line("Holdout R²", f"{m.get('holdout_r2', 0):.4f}"))
    print(line("Holdout MAE", f"{m.get('holdout_mae', 0):.6f}"))
    print(line("Full-fit R²", f"{m.get('full_fit_r2', 0):.4f}"))
    print(line("Full-fit MAE", f"{m.get('full_fit_mae', 0):.6f}"))
    print("  ╠══════════════════════════════════════════════════════════╣")
    print("  ║  Estimators: HistGradientBoosting + GradientBoosting     ║")
    print("  ║  Artifact:   models/model_bundle.joblib                  ║")
    print("  ╚══════════════════════════════════════════════════════════╝")
    print("")
