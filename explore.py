from sklearn.datasets import fetch_california_housing
import pandas as pd

data = fetch_california_housing()

df = pd.DataFrame(data.data, columns=data.feature_names)

df["Price"] = data.target

print("Shape of the dataset:", df.shape)

print("Total records in the dataset:", df.shape[0])

print(df.head())

print(df.describe())
