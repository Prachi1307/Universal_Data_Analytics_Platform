import joblib
import numpy as np

from sklearn.ensemble import RandomForestClassifier

from utils.database import get_all_data


def train_model():

    df = get_all_data()

    if len(df) < 20:
        return False

    if "failure" not in df.columns:

        df["failure"] = np.where(

            (df["temperature"] > df["temperature"].mean()) &
            (df["vibration"] > df["vibration"].mean()),

            1,

            0

        )

    features = [

        "temperature",
        "pressure",
        "vibration",
        "humidity",
        "power",
        "production"

    ]

    X = df[features]

    y = df["failure"]

    model = RandomForestClassifier(

        n_estimators=200,

        random_state=42

    )

    model.fit(X, y)

    joblib.dump(model, "models/factory_model.pkl")

    return True


if __name__ == "__main__":
    train_model()