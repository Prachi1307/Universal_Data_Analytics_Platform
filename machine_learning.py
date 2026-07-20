import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor

from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

from sklearn.svm import SVC
from sklearn.svm import SVR

from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor

from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


def machine_learning_page():
    st.title("🤖 Machine Learning")

    if "df" not in st.session_state:
        st.warning("Upload dataset first.")
        return

    df = st.session_state.df.copy()

    if df.empty:
        st.warning("Dataset is empty.")
        return

    df = df.dropna().copy()

    for col in df.select_dtypes(include=["object", "category"]).columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    columns = df.columns.tolist()

    st.sidebar.header("Model Settings")

    target = st.sidebar.selectbox(
        "Target Column",
        columns
    )

    features = st.sidebar.multiselect(
        "Feature Columns",
        [c for c in columns if c != target],
        default=[c for c in columns if c != target]
    )

    if len(features) == 0:
        st.warning("Select feature columns.")
        return

    X = df[features]
    y = df[target]

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    if y.nunique() <= 20:
        problem_type = "Classification"
    else:
        problem_type = "Regression"

    st.info(f"Detected Problem Type : {problem_type}")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    if problem_type == "Classification":
        model_name = st.selectbox(
            "Algorithm",
            [
                "Logistic Regression",
                "Decision Tree",
                "Random Forest",
                "Support Vector Machine",
                "KNN",
                "Naive Bayes"
            ]
        )
    else:
        model_name = st.selectbox(
            "Algorithm",
            [
                "Linear Regression",
                "Decision Tree",
                "Random Forest",
                "Support Vector Regression",
                "KNN Regressor"
            ]
        )

    train = st.button(
        "🚀 Train Model",
        use_container_width=True
    )

    if train:
        if problem_type == "Classification":
            if model_name == "Logistic Regression":
                model = LogisticRegression(max_iter=500)

            elif model_name == "Decision Tree":
                model = DecisionTreeClassifier(random_state=42)

            elif model_name == "Random Forest":
                model = RandomForestClassifier(random_state=42)

            elif model_name == "Support Vector Machine":
                model = SVC()

            elif model_name == "KNN":
                model = KNeighborsClassifier()

            elif model_name == "Naive Bayes":
                model = GaussianNB()
        else:
            if model_name == "Linear Regression":
                model = LinearRegression()

            elif model_name == "Decision Tree":
                model = DecisionTreeRegressor(random_state=42)

            elif model_name == "Random Forest":
                model = RandomForestRegressor(random_state=42)

            elif model_name == "Support Vector Regression":
                model = SVR()

            elif model_name == "KNN Regressor":
                model = KNeighborsRegressor()

        model.fit(
            X_train,
            y_train
        )

        prediction = model.predict(
            X_test
        )

        st.success("✅ Model trained successfully.")
        st.divider()

        if problem_type == "Classification":
            accuracy = accuracy_score(y_test, prediction)
            precision = precision_score(
                y_test,
                prediction,
                average="weighted",
                zero_division=0
            )
            recall = recall_score(
                y_test,
                prediction,
                average="weighted",
                zero_division=0
            )
            f1 = f1_score(
                y_test,
                prediction,
                average="weighted",
                zero_division=0
            )

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Accuracy", f"{accuracy:.4f}")
            c2.metric("Precision", f"{precision:.4f}")
            c3.metric("Recall", f"{recall:.4f}")
            c4.metric("F1 Score", f"{f1:.4f}")

            cm = confusion_matrix(
                y_test,
                prediction
            )

            fig = px.imshow(
                cm,
                text_auto=True,
                title="Confusion Matrix",
                color_continuous_scale="Blues"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
        else:
            mae = mean_absolute_error(
                y_test,
                prediction
            )
            mse = mean_squared_error(
                y_test,
                prediction
            )
            rmse = np.sqrt(mse)
            r2 = r2_score(
                y_test,
                prediction
            )

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("MAE", f"{mae:.4f}")
            c2.metric("MSE", f"{mse:.4f}")
            c3.metric("RMSE", f"{rmse:.4f}")
            c4.metric("R² Score", f"{r2:.4f}")

            result = pd.DataFrame({
                "Actual": y_test,
                "Predicted": prediction
            })

            fig = px.scatter(
                result,
                x="Actual",
                y="Predicted",
                trendline="ols",
                title="Actual vs Predicted"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.divider()
        st.subheader("Prediction Results")

        results = pd.DataFrame({
            "Actual": y_test,
            "Predicted": prediction
        })

        st.dataframe(
            results,
            use_container_width=True
        )

        csv = results.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Predictions",
            csv,
            "predictions.csv",
            "text/csv",
            use_container_width=True
        )

        st.divider()
        st.subheader("Feature Importance")

        if hasattr(model, "feature_importances_"):
            importance = pd.DataFrame({
                "Feature": features,
                "Importance": model.feature_importances_
            }).sort_values(
                by="Importance",
                ascending=False
            )

            st.dataframe(
                importance,
                use_container_width=True
            )

            fig = px.bar(
                importance,
                x="Feature",
                y="Importance",
                color="Importance",
                title="Feature Importance"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        elif hasattr(model, "coef_"):
            importance = pd.DataFrame({
                "Feature": features,
                "Coefficient": (
                    model.coef_.flatten()
                    if len(np.array(model.coef_).shape) > 1
                    else model.coef_
                )
            })

            st.dataframe(
                importance,
                use_container_width=True
            )

            fig = px.bar(
                importance,
                x="Feature",
                y="Coefficient",
                color="Coefficient",
                title="Feature Coefficients"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
        else:
            st.info("Feature importance is not available for this model.")

        st.success("✅ Machine Learning analysis completed successfully.")