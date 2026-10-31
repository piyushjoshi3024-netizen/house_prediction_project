# 🏠 House Prediction API

A machine-learning-powered REST API built with **FastAPI** that predicts California house values using a trained **Scikit-learn Random Forest Regressor**.

The API validates incoming house features, generates predictions using the trained ML model, and stores prediction history in **PostgreSQL**.

---

## 🚀 Current Project Status

The project has progressed from a standalone ML model to a complete backend API.

### Completed

* ✅ California Housing dataset exploration
* ✅ Random Forest Regression model
* ✅ Model evaluation using MAE and R²
* ✅ Model serialization using Joblib
* ✅ FastAPI application
* ✅ Pydantic request validation
* ✅ `POST /predict`
* ✅ Health-check endpoint
* ✅ PostgreSQL integration
* ✅ SQLAlchemy ORM
* ✅ Prediction history storage
* ✅ `GET /predictions`
* ✅ `GET /predictions/{id}`
* ✅ `DELETE /predictions/{id}`
* ✅ Automated API tests with Pytest
* ✅ Application logging
* ✅ Improved API error handling
* ✅ ML prediction logic separated into a service layer
* ✅ Environment configuration using `.env`
* ✅ Git/GitHub workflow

### Currently Working On

* 🔄 Router separation
* 🔄 Improving project architecture

---

## 🏗️ Architecture

```text
Client
  │
  ▼
FastAPI
  │
  ├── Pydantic Validation
  │
  ▼
Prediction Service
  │
  ▼
Scikit-learn Model
  │
  ▼
Predicted House Value
  │
  ▼
SQLAlchemy
  │
  ▼
PostgreSQL
```

The project is gradually being organized into separate layers for API routes, schemas, services, database access, and configuration.

---

## 📁 Project Structure

```text
fast_api_proj-2/
│
├── main.py
├── train.py
├── explore.py
├── schemas.py
├── database.py
├── models.py
├── config.py
├── init_db.py
├── test_main.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── services/
│   ├── __init__.py
│   └── prediction_service.py
│
├── routers/
│   ├── __init__.py
│   └── predictions.py
│
├── california_housing_model.pkl
└── model_columns.pkl
```

> `.pkl` model files are generated locally and are excluded from Git.

---

## 🧠 Machine Learning Model

The project uses the **California Housing dataset** provided by Scikit-learn.

### Model

```text
RandomForestRegressor
```

### Input Features

The model uses eight features:

| Feature      | Description                              |
| ------------ | ---------------------------------------- |
| `MedInc`     | Median income in the block group         |
| `HouseAge`   | Median house age                         |
| `AveRooms`   | Average number of rooms per household    |
| `AveBedrms`  | Average number of bedrooms per household |
| `Population` | Block group population                   |
| `AveOccup`   | Average household occupancy              |
| `Latitude`   | Geographic latitude                      |
| `Longitude`  | Geographic longitude                     |

The model predicts the **median house value** for a California geographic block group.

---

## 🔌 API Endpoints

### `GET /`

Returns basic API information.

### `GET /health`

Checks whether the API is running.

### `POST /predict`

Generates a house-value prediction.

Example request:

```json
{
  "MedInc": 8.3252,
  "HouseAge": 41,
  "AveRooms": 6.9841,
  "AveBedrms": 1.0238,
  "Population": 322,
  "AveOccup": 2.5556,
  "Latitude": 37.88,
  "Longitude": -122.23
}
```

### `GET /predictions`

Returns stored prediction history.

### `GET /predictions/{prediction_id}`

Returns a specific prediction.

Example:

```text
GET /predictions/1
```

### `DELETE /predictions/{prediction_id}`

Deletes a stored prediction.

Example:

```text
DELETE /predictions/1
```

---

## 🗄️ PostgreSQL

Prediction results are persisted in PostgreSQL.

```text
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
   ↓
predictions table
```

The stored data includes:

* Input features
* Predicted price
* Prediction ID
* Creation timestamp

Database configuration is loaded through the `.env` file.

---

## 🧪 Testing

Automated API tests are implemented using:

Pytest
FastAPI TestClient

Run:

```powershell
pytest
```

The tests cover:

* API health
* Root endpoint
* Successful prediction
* Invalid input validation
* Prediction API behavior

---

## 📊 Logging & Error Handling

The API uses Python's `logging` module to record important events such as:

```text
Prediction request received
Prediction saved successfully
Prediction deleted successfully
Prediction failed
```

Unexpected server errors are logged with their technical details while the API returns a safe response to the client.

Example:

```json
{
  "detail": "Prediction failed. Please try again later."
}
```

---

## ⚙️ Local Setup

### 1. Clone the repository

```powershell
git clone https://github.com/piyushjoshi3024-netizen/house_prediction_project.git
cd house_prediction_project
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create the database:

```sql
CREATE DATABASE house_prediction_db;
```

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/house_prediction_db
```

### 5. Create database tables

```powershell
python init_db.py
```

### 6. Generate the ML model

If the model artifacts are not present locally:

```powershell
python train.py
```

This generates:

```text
california_housing_model.pkl
model_columns.pkl
```

### 7. Start the API

```powershell
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🔐 Git & Model Files

The trained model is approximately 138 MB and therefore is **not committed to GitHub**.

The following files are ignored:

```text
*.pkl
*.joblib
.env
venv/
__pycache__/
.pytest_cache/
```

Run:

```powershell
python train.py
```

to regenerate the model artifacts locally.

A production-ready model artifact strategy will be added later.

---

# 🛣️ Roadmap

The project is being developed progressively from a working ML API into a production-oriented backend.

### Architecture

* 🔄 Complete service/router separation
* ⏳ Database migrations with Alembic

### Infrastructure

* ⏳ Dockerize the API
* ⏳ Configure CI/CD
* ⏳ Deploy the API

### Security (THOUGH THIS ONE IS OPTIONAL ,IT IF IT MAKES SENSE , I'LL PUT IT ; IF NOT ,I'LL IGNORE IT ; DEPENDS ON THE ARCHITECTURE AND FUTURE DIRECTION OF THIS PROJECT )

* ⏳ Authentication and JWT authorization 

### ML Productionization

* ⏳ Production ML artifact/model storage strategy

---

## 🛠️ Tech Stack

**Backend**

* Python
* FastAPI
* Pydantic
* SQLAlchemy

**Machine Learning**

* Scikit-learn
* Pandas
* Joblib

**Database**

* PostgreSQL
* Psycopg

**Testing**

* Pytest
* FastAPI TestClient

**Development**

* Uvicorn
* Git
* GitHub

---

## ⚠️ Disclaimer

This project predicts median house values using the California Housing dataset.

The prediction is a **machine-learning project estimate** and should not be treated as a real-world property valuation or professional appraisal.
