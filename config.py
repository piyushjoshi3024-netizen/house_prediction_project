from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "california_housing_model.pkl"
COLUMNS_PATH = BASE_DIR / "model_columns.pkl"