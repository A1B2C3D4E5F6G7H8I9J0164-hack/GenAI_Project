#!/usr/bin/env python3
"""
Ensure model files are ready before starting the server.

Run this script during the build/startup process on Render.
It handles three scenarios:
  1. Model bundle already exists → skip (fast path)
  2. Training CSV data exists but no model → train from data
  3. Neither model nor CSV data exist → generate synthetic data, then train

This guarantees the API can serve predictions on first request.
"""

import os
import sys

# Add backend to path so ml package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def ensure_model_ready():
    """Ensure model_bundle.joblib exists; train or generate if needed."""
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(backend_dir, "models")
    bundle_path = os.path.join(models_dir, "model_bundle.joblib")
    data_dir = os.path.join(backend_dir, "data")

    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    # Check scikit-learn version
    try:
        import sklearn
        print(f"📦 Active scikit-learn version: {sklearn.__version__}")
    except ImportError:
        pass

    # Fast path: model already exists
    if os.path.isfile(bundle_path):
        size_mb = os.path.getsize(bundle_path) / (1024 * 1024)
        print(f"✅ Model bundle exists: {bundle_path} ({size_mb:.1f} MB)")
        return True

    print("⚠️  Model bundle not found. Attempting to create...")

    # Check for training data
    import glob
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))

    if not csv_files:
        print("📊 No CSV training data found. Generating synthetic data...")
        try:
            from ml.generate_synthetic import generate_synthetic_csv
            generate_synthetic_csv(data_dir)
            csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
            print(f"✅ Generated synthetic data: {len(csv_files)} file(s)")
        except Exception as e:
            print(f"❌ Synthetic data generation failed: {e}")
            import traceback
            traceback.print_exc()
            return False

    # Train model from available data
    print("🔧 Training model from data...")
    try:
        from ml.train import train_and_save_bundle
        bundle = train_and_save_bundle(backend_dir, force_refresh_data=True)
        metrics = bundle.get("metrics", {})
        print(f"✅ Model trained successfully!")
        print(f"   R² = {metrics.get('holdout_r2', 'N/A')}")
        print(f"   MAE = {metrics.get('holdout_mae', 'N/A')}")
        print(f"   Rows = {metrics.get('n_rows', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        success = ensure_model_ready()
        if success:
            print("✓ Model ready for serving")
            sys.exit(0)
        else:
            print("⚠ Model preparation had issues, but server will start with fallback", file=sys.stderr)
            sys.exit(0)  # Don't block startup — fallback predictor handles it
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(0)  # Still don't block — let the server start
