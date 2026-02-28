import pandas as pd

df = pd.read_csv("data/train.csv")

print("Shape of dataset:", df.shape)

print("\nTop 10 Missing Values:")
print(df.isnull().sum().sort_values(ascending=False).head(10))

print("\nTarget Column Check:")
print(df["SalePrice"].describe())

print("\nTop 10 Correlated Features with SalePrice:")
correlation = df.corr(numeric_only=True)["SalePrice"].sort_values(ascending=False)
print(correlation.head(10))