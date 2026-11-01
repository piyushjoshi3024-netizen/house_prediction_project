import joblib
import pandas as pd

from config import MODEL_PATH, COLUMNS_PATH


model = joblib.load(MODEL_PATH)
model_columns = joblib.load(COLUMNS_PATH)


def predict_house_price(features: dict) -> float:
    input_data = pd.DataFrame([features])

    input_data = input_data[model_columns]

    prediction = model.predict(input_data)

    predicted_price = prediction[0] * 100000

    return float(predicted_price)