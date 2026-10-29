from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json()["status"] == "Running"
    
def test_health_check():
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict():
    
    payload = {
        "MedInc": 5.0,
        "HouseAge": 20.0,
        "AveRooms": 6.0,
        "AveBedrms": 1.0,
        "Population": 1000.0,
        "AveOccup": 3.0,
        "Latitude": 34.0,
        "Longitude": -118.0
    }
    
    response = client.post("/predict", json = payload)
    
    assert response.status_code == 200
    assert "predicted_price" in response.json()
    assert response.json()["status"] == "Prediction successful"
    
    
def test_predict_invalid_input():
    payload = {
        "MedInc": -1,
        "HouseAge": 41,
        "AveRooms":6.98,
        "AveBedrms": 1.0,
        "Population": 1000.0,
        "AveOccup": 3.0,
        "Latitude": 34.0,
        "Longitude": -118.0
    }
    
    response = client.post("/predict", json=payload)

    assert response.status_code == 422