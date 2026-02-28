# model.py

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score

# Load cleaned data
df = pd.read_csv("data/train_cleaned.csv")

X = df.drop("SalePrice", axis=1)
y = df["SalePrice"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)

print("R2 Score:", r2_score(y_test, pred))

cv_score = cross_val_score(model, X, y, cv=5)
print("Cross Validation Score:", cv_score.mean())

# Save model
joblib.dump(model, "model.pkl")

print("✅ Model Saved")