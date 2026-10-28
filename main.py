import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="California Housing Price Prediction API", version="1.0")

model = joblib.load("california_housing_model.pkl")
model_columns = joblib.load("C:\\Users\\Piyus\\OneDrive\\Documents\\fast_api_proj-2\\model_columns.pkl")

# here we have to put the INPUT SCHEMA for the API, which is the same as the features used in the model training

class HouseFeatures(BaseModel):
    MedInc: float = Field(gt=0, description="Median income in block group")
    HouseAge: float = Field(ge=0, description="Median house age in block group")
    AveRooms: float = Field(gt=0, description="Average number of rooms per household")
    AveBedrms: float = Field(gt=0, description="Average number of bedrooms per household")
    Population: float = Field(ge=0, description="Block group population")
    AveOccup: float = Field(gt=0, description="Average number of household members")
    Latitude: float = Field(ge=-90, le=90, description="Block group latitude")
    Longitude: float = Field(ge=-180, le=180, description="Block group longitude")

features = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
]


#home
@app.get("/")
def home():
    return {"message": "Welcome to the California Housing Price Prediction API!",
            "status_code": 200,
            "status": "Running",
            "description": "This API predicts the median house value in California based on various features.",
            "endpoints": "send Post request to /predict with the required features in JSON format to get the predicted house price."
            }
    
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "The API is running smoothly.",
            "status_code": 200,
            "model":"Random Forest Regressor",
            "features": features,
            "avg error": "$39000"
            }
    
    
@app.post("/predict")
def predict_price(features: HouseFeatures):
    """Predict the price of a house based on its features."""
    try:
       input_data = pd.DataFrame([features.dict()])
       
       
       prediction = model.predict(input_data)
       predicted_price = prediction[0] * 100000  # Convert to dollars
       
       return {
           "predicted_price": f"${predicted_price:,.2f}",
           "status_code": 200,
           "status": "Prediction successful",
              "input_features": features.dict()
         }
       
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
        status_code = 500
        detail = f"Prediction failed: {str(e)}" 