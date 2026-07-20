import streamlit as st
import pandas as pd


def home_page():

    st.markdown(
        """
        <div class="glass">
            <h2>🚀 Welcome to Universal Data Analytics Platform</h2>
            <p>
            Upload any dataset and generate dashboards, analytics,
            machine learning models, reports and interactive visualizations
            without writing a single line of code.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if st.session_state.df is None:

        st.info("👈 Start by uploading a CSV, Excel, JSON or Parquet file.")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(
                """
                ### 📂 Upload

                • CSV

                • Excel

                • JSON

                • Parquet
                """
            )

        with c2:

            st.markdown(
                """
                ### 📈 Analyze

                • Statistics

                • Correlation

                • Missing Values

                • Outliers
                """
            )

        with c3:

            st.markdown(
                """
                ### 🤖 Machine Learning

                • Classification

                • Regression

                • Clustering

                • Feature Importance
                """
            )

        st.divider()

        st.subheader("✨ Platform Features")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.success("✔ 30+ Charts")

        with col2:
            st.success("✔ Auto Column Detection")

        with col3:
            st.success("✔ AI Insights")

        with col4:
            st.success("✔ PDF Reports")

        return

    df = st.session_state.df

    rows = len(df)
    cols = len(df.columns)

    numeric = len(df.select_dtypes(include="number").columns)

    categorical = len(
        df.select_dtypes(include=["object", "category"]).columns
    )

    dates = len(
        df.select_dtypes(include=["datetime64", "datetime64[ns]"]).columns
    )

    missing = int(df.isna().sum().sum())

    duplicates = int(df.duplicated().sum())

    st.success("Dataset Loaded Successfully")

    a, b, c, d = st.columns(4)

    a.metric("Rows", f"{rows:,}")

    b.metric("Columns", cols)

    c.metric("Missing Values", missing)

    d.metric("Duplicate Rows", duplicates)

    st.write("")

    a, b, c = st.columns(3)

    a.metric("Numeric Columns", numeric)

    b.metric("Categorical Columns", categorical)

    c.metric("Date Columns", dates)

    st.divider()

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("Detected Columns")

    left, right = st.columns(2)

    with left:

        st.markdown("### 🔢 Numeric")

        nums = df.select_dtypes(include="number").columns.tolist()

        if nums:
            st.write(nums)
        else:
            st.warning("No Numeric Columns")

    with right:

        st.markdown("### 📝 Categorical")

        cats = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        if cats:
            st.write(cats)
        else:
            st.warning("No Categorical Columns")

    st.divider()

    st.subheader("Column Information")

    info = pd.DataFrame({

        "Column": df.columns,

        "Datatype": df.dtypes.astype(str),

        "Missing": df.isna().sum().values,

        "Unique Values": df.nunique().values

    })

    st.dataframe(
        info,
        use_container_width=True,
        hide_index=True,
    )