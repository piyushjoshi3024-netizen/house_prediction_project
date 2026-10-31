import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import logging
from sqlalchemy.orm import Session

from database import get_db
from models import Prediction

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



model = joblib.load("california_housing_model.pkl")
model_columns = joblib.load("C:\\Users\\Piyus\\OneDrive\\Documents\\fast_api_proj-2\\model_columns.pkl")

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

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
def predict_price(
    features: HouseFeatures,
    db: Session = Depends(get_db)
):
    try:
        logger.info("Prediction request received")

        input_data = pd.DataFrame([features.model_dump()])
        prediction = model.predict(input_data)

        predicted_price = prediction[0] * 100000

        new_prediction = Prediction(
            MedInc=features.MedInc,
            HouseAge=features.HouseAge,
            AveRooms=features.AveRooms,
            AveBedrms=features.AveBedrms,
            Population=features.Population,
            AveOccup=features.AveOccup,
            Latitude=features.Latitude,
            Longitude=features.Longitude,
            predicted_price=float(predicted_price)
        )

        db.add(new_prediction)
        db.commit()
        db.refresh(new_prediction)

        logger.info("Prediction saved to database")

        return {
            "predicted_price": f"${predicted_price:,.2f}",
            "prediction_id": new_prediction.id,
            "status_code": 200,
            "status": "Prediction successful",
            "input_features": features.model_dump()
        }
    

    except Exception as e:
        db.rollback()
        logger.error(f"Prediction failed: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Prediction failed"
        )
        
        
@app.get("/predictions")
def get_predictions(db: Session = Depends(get_db)):
    predictions = db.query(Prediction).all()

    return {
        "status": "success",
        "count": len(predictions),
        "predictions": [
            {
                "id": prediction.id,
                "MedInc": prediction.MedInc,
                "HouseAge": prediction.HouseAge,
                "AveRooms": prediction.AveRooms,
                "AveBedrms": prediction.AveBedrms,
                "Population": prediction.Population,
                "AveOccup": prediction.AveOccup,
                "Latitude": prediction.Latitude,
                "Longitude": prediction.Longitude,
                "predicted_price": prediction.predicted_price,
                "created_at": prediction.created_at
            }
            for prediction in predictions
        ]
    }      


        
@app.get("/predictions/{prediction_id}")
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    prediction = (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id)
        .first()
    )

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    return {
        "status": "success",
        "prediction": {
            "id": prediction.id,
            "MedInc": prediction.MedInc,
            "HouseAge": prediction.HouseAge,
            "AveRooms": prediction.AveRooms,
            "AveBedrms": prediction.AveBedrms,
            "Population": prediction.Population,
            "AveOccup": prediction.AveOccup,
            "Latitude": prediction.Latitude,
            "Longitude": prediction.Longitude,
            "predicted_price": prediction.predicted_price,
            "created_at": prediction.created_at
        }
    }


@app.delete("/predictions/{prediction_id}")
def delete_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    prediction = (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id)
        .first()
    )

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    db.delete(prediction)
    db.commit()

    return {
        "status": "success",
        "message": "Prediction deleted successfully",
        "prediction_id": prediction_id
    }