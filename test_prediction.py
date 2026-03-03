from services.prediction import predict_price

sample_data = {
    "bedrooms": 3,
    "bathrooms": 2,
    "sqft_living": 1800,
    "grade": 7,
    "condition": 3,
    "yr_built": 2000,
    "lat": 47.5112,
    "long": -122.257,
    "year_sold": 2015
}

predicted_price = predict_price(sample_data)

print("Predicted Price:", predicted_price)