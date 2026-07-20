import os
import joblib
import pandas as pd

MODEL = "models/factory_model.pkl"

FEATURES = [

    "temperature",
    "pressure",
    "vibration",
    "humidity",
    "power",
    "production"

]


def load_model():

    if not os.path.exists(MODEL):

        return None

    return joblib.load(MODEL)


def predict_failure(data):

    model = load_model()

    if model is None:

        return None, None

    sample = pd.DataFrame([data], columns=FEATURES)

    prediction = model.predict(sample)[0]

    probability = model.predict_proba(sample)[0][1]

    return prediction, probability