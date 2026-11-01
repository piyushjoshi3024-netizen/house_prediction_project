import logging

from fastapi import FastAPI

from routers import predictions


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="California Housing Price Prediction API",
    version="1.0"
)


app.include_router(predictions.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the California Housing Price Prediction API!",
        "status_code": 200,
        "status": "Running",
        "description": "This API predicts the median house value in California based on various features.",
        "endpoints": "send Post request to /predict with the required features in JSON format to get the predicted house price."
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "The API is running smoothly.",
        "status_code": 200,
        "model": "Random Forest Regressor",
        "features": [
            "MedInc",
            "HouseAge",
            "AveRooms",
            "AveBedrms",
            "Population",
            "AveOccup",
            "Latitude",
            "Longitude"
        ],
        "avg error": "$39000"
    }