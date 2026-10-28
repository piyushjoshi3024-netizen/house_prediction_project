from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd
import joblib

print("Loading the California housing dataset...")

data = fetch_california_housing()

X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

print("Total records in the dataset:", X.shape[0])
print("Shape of the dataset:", X.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train the Random Forest Regressor model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Predict house values for the test set
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# The target is measured in units of $100,000
print(f"Average error: ${mae * 100000:,.2f}")
print("R-squared score:", r2)

# Save the trained model and feature columns
joblib.dump(model, "california_housing_model.pkl")
joblib.dump(list(X.columns), "model_columns.pkl")

