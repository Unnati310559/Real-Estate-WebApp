# preprocessing.py

import pandas as pd
import numpy as np

# Load raw dataset
df = pd.read_csv("data/train.csv")

# -----------------------------
# 1️⃣ Remove Outliers
# -----------------------------
df = df[df["GrLivArea"] < 4000]

# -----------------------------
# 2️⃣ Log Transform Target
# -----------------------------
df["SalePrice"] = np.log1p(df["SalePrice"])

# -----------------------------
# 3️⃣ Handle Missing Values
# -----------------------------
num_cols = df.select_dtypes(include=["int64", "float64"]).columns
for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

cat_cols = df.select_dtypes(include=["object"]).columns
for col in cat_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# -----------------------------
# 4️⃣ Feature Engineering
# -----------------------------
df["TotalSF"] = df["TotalBsmtSF"] + df["1stFlrSF"] + df.get("2ndFlrSF", 0)

# -----------------------------
# 5️⃣ Encoding
# -----------------------------
df = pd.get_dummies(df, drop_first=True)

# Save cleaned data
df.to_csv("data/train_cleaned.csv", index=False)

print("✅ Preprocessing Completed")