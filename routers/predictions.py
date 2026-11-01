from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Prediction
from schemas import HouseFeatures
from services.prediction_service import predict_house_price


router = APIRouter(
    tags=["Predictions"]
)


@router.post("/predict")
def predict_price(
    features: HouseFeatures,
    db: Session = Depends(get_db)
):
    try:
        predicted_price = predict_house_price(
            features.model_dump()
        )

        new_prediction = Prediction(
            MedInc=features.MedInc,
            HouseAge=features.HouseAge,
            AveRooms=features.AveRooms,
            AveBedrms=features.AveBedrms,
            Population=features.Population,
            AveOccup=features.AveOccup,
            Latitude=features.Latitude,
            Longitude=features.Longitude,
            predicted_price=predicted_price
        )

        db.add(new_prediction)
        db.commit()
        db.refresh(new_prediction)

        return {
            "predicted_price": f"${predicted_price:,.2f}",
            "prediction_id": new_prediction.id,
            "status_code": 200,
            "status": "Prediction successful",
            "input_features": features.model_dump()
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Please try again later."
        )


@router.get("/predictions")
def get_predictions(
    db: Session = Depends(get_db)
):
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


@router.get("/predictions/{prediction_id}")
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


@router.delete("/predictions/{prediction_id}")
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

    try:
        db.delete(prediction)
        db.commit()

        return {
            "status": "success",
            "message": "Prediction deleted successfully",
            "prediction_id": prediction_id
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete prediction"
        )