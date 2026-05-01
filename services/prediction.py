import joblib
import os
import gdown

model = None

def load_model():
    global model

    if model is None:
        # ✅ Correct path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(BASE_DIR, "models", "price_model.pkl")

        # ✅ Download if not exists
        if not os.path.exists(model_path):
            os.makedirs(os.path.dirname(model_path), exist_ok=True)

            file_id = "1lsbY0WnZpz2YdxQ8e47YPp1aT4opRxtZ"
            url = f"https://drive.google.com/uc?id={file_id}"

            gdown.download(url, model_path, quiet=False)

        # ✅ Load model (with error handling)
        try:
            model = joblib.load(model_path)
        except Exception as e:
            print("Error loading model:", e)

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
