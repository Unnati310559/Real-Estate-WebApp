# =========================================
# REAL ESTATE PRICE PREDICTION TRAINING
# =========================================

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error


# =========================================
# LOAD DATASET
# =========================================

df = pd.read_csv("kc_house_data(1).csv")

print("Dataset Loaded Successfully")
print("Shape:", df.shape)


# =========================================
# DATA CLEANING
# =========================================

# Drop unnecessary column
df = df.drop(columns=["id"])

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Extract year
df["year_sold"] = df["date"].dt.year

# Drop original date
df = df.drop(columns=["date"])

# Remove extreme outliers
df = df[df["price"] < 5000000]
df = df[df["sqft_living"] < 10000]

print("Cleaning Done")
print("Shape after cleaning:", df.shape)


# =========================================
# FEATURE SELECTION
# =========================================

features = [
    "bedrooms",
    "bathrooms",
    "sqft_living",
    "grade",
    "condition",
    "yr_built",
    "lat",
    "long",
    "year_sold"
]

X = df[features]
y = df["price"]


# =========================================
# TRAIN TEST SPLIT
# =========================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# =========================================
# TRAIN MODEL
# =========================================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

print("Model Training Completed")


# =========================================
# MODEL EVALUATION
# =========================================

y_pred = model.predict(X_test)

r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\nModel Performance:")
print("R2 Score:", r2)
print("MAE:", mae)
print("RMSE:", rmse)


# =========================================
# SAVE MODEL
# =========================================

joblib.dump(model, "models/price_model.pkl")

print("\nModel Saved Successfully!")