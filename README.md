# House Prediction API

A machine-learning API that serves predictions from a trained Scikit-learn model using FastAPI.

## Current Progress

* Explored the California Housing dataset.
* Trained a `RandomForestRegressor`.
* Evaluated the model using MAE and R².
* Saved the trained model and feature columns locally.
* Building the FastAPI endpoint to accept housing features and return a prediction.

## Tech Stack

Python · Scikit-learn · Pandas · FastAPI · Pydantic · Joblib · Uvicorn

## Run Locally

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install fastapi uvicorn pandas scikit-learn joblib
```

Generate the model:

```powershell
python train.py
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Model Artifacts

The generated `.pkl` files are kept locally and excluded from Git. Run `python train.py` to regenerate them.

> The model uses the California Housing dataset and estimates median house value for a geographic block group. It is a project/demo estimate, not a live appraisal of an individual property.
