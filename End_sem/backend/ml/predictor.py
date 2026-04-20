import os
from typing import Any, Dict, List, Optional, Tuple, Union

import joblib
import numpy as np
import pandas as pd

from .feature_columns import build_manual_feature_vector
from .train import train_and_save_bundle

_bundle: Optional[Dict[str, Any]] = None


def _backend_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _bundle_path() -> str:
    return os.path.join(_backend_dir(), "models", "model_bundle.joblib")


def ensure_model_trained() -> None:
    """Train (or retrain) if bundle missing."""
    if not os.path.isfile(_bundle_path()):
        print("Model bundle not found. Training from data/ ...")
        train_and_save_bundle(_backend_dir(), force_refresh_data=False)


def load_bundle() -> Dict[str, Any]:
    global _bundle
    if _bundle is not None:
        return _bundle

    ensure_model_trained()
    
    try:
        _bundle = joblib.load(_bundle_path())
        return _bundle
    except AttributeError as e:
        # Handle scikit-learn version mismatch
        if "sklearn" in str(e) or "__pyx_unpickle" in str(e):
            print(f"⚠️ scikit-learn version mismatch: {e}")
            print("🔄 Attempting to retrain model...")
            
            # Delete incompatible bundle
            bundle_path = _bundle_path()
            if os.path.isfile(bundle_path):
                os.remove(bundle_path)
                print(f"Deleted incompatible bundle: {bundle_path}")
            
            # Retrain with current environment
            try:
                train_and_save_bundle(_backend_dir(), force_refresh_data=False)
                _bundle = joblib.load(_bundle_path())
                print("✅ Model successfully retrained and loaded")
                return _bundle
            except Exception as retrain_err:
                print(f"❌ Retraining failed: {retrain_err}")
                # Return fallback bundle with dummy estimator
                return _get_fallback_bundle()
        else:
            raise


def _get_fallback_bundle() -> Dict[str, Any]:
    """Fallback bundle with simple mean-based predictor."""
    import warnings
    warnings.filterwarnings('ignore')
    
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    
    class SimpleMeanPredictor:
        """Fallback predictor that returns mean value."""
        def __init__(self):
            self.mean_value = 0.25
        
        def predict(self, X):
            # Return a reasonable default prediction
            return np.full(len(X), self.mean_value)
        
        def fit(self, X, y):
            if len(y) > 0:
                self.mean_value = float(np.mean(y))
            return self
    
    return {
        "estimator": SimpleMeanPredictor(),
        "scaler": StandardScaler(),
        "feature_columns": [
            'Hour', 'DayOfWeek', 'Demand_Lag_1', 'Demand_Lag_2',
            'Rolling_Avg_3h', 'Electricity Price ($/kWh)',
            'Grid Stability Index', 'Number of EVs Charging'
        ],
        "defaults": {}
    }


def load_model():
    """
    Backwards-compatible: returns (estimator, scaler) tuple.
    Estimator is WeightedEnsemble with .predict.
    """
    b = load_bundle()
    return b["estimator"], b["scaler"]


def get_feature_columns() -> List[str]:
    b = load_bundle()
    return list(b["feature_columns"])


def get_defaults() -> Dict[str, float]:
    b = load_bundle()
    return dict(b.get("defaults", {}))


def predict_single(features: dict) -> float:
    b = load_bundle()
    model = b["estimator"]
    scaler = b["scaler"]
    columns: List[str] = b["feature_columns"]
    defaults: Dict[str, float] = b.get("defaults", {})

    row = build_manual_feature_vector(features, defaults, columns)
    X = pd.DataFrame([row], columns=columns)
    if scaler is not None:
        X = scaler.transform(X)
    else:
        X = X.to_numpy(dtype=float)
    return float(model.predict(X)[0])


def predict_batch(X: Union[np.ndarray, pd.DataFrame]) -> np.ndarray:
    b = load_bundle()
    model = b["estimator"]
    scaler = b["scaler"]
    cols: List[str] = b["feature_columns"]
    if isinstance(X, np.ndarray):
        X = pd.DataFrame(X, columns=cols)
    if scaler is not None:
        X = scaler.transform(X)
    elif hasattr(X, "to_numpy"):
        X = X.to_numpy(dtype=float)
    return model.predict(X)


def auto_generate_model(base_dir: str) -> None:
    """Used if legacy code paths call this; trains full bundle from all data files."""
    train_and_save_bundle(base_dir, force_refresh_data=True)
