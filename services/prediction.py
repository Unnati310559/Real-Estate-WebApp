import joblib
import os

model = None

def load_model():
    global model

    if model is None:
        model_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "models",
            "price_model.pkl"
        )
        model_path = os.path.abspath(model_path)

        model = joblib.load(model_path)

    return model


def predict_price(data):

    model = load_model()

    features = [[
        data["bedrooms"],
        data["bathrooms"],
        data["sqft_living"],
        data["grade"],
        data["condition"],
        data["yr_built"],
        data["lat"],
        data["long"],
        data["year_sold"]
    ]]

    return model.predict(features)[0]