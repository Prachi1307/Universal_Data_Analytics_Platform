import streamlit as st
import pandas as pd


def profile_page():
    st.title("👤 Dataset Profile")

    if "df" not in st.session_state:
        st.warning("Upload a dataset first.")
        return

    df = st.session_state.df.copy()

    rows, cols = df.shape

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    datetime_cols = df.select_dtypes(
        include=["datetime", "datetime64[ns]"]
    ).columns.tolist()

    bool_cols = df.select_dtypes(include="bool").columns.tolist()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", rows)
    c2.metric("Columns", cols)
    c3.metric("Numeric", len(numeric_cols))
    c4.metric("Categorical", len(categorical_cols))

    st.divider()

    st.subheader("Dataset Information")

    info = pd.DataFrame({
        "Property": [
            "Rows",
            "Columns",
            "Memory Usage (MB)",
            "Missing Values",
            "Duplicate Rows"
        ],
        "Value": [
            rows,
            cols,
            round(df.memory_usage(deep=True).sum() / 1024**2, 2),
            int(df.isna().sum().sum()),
            int(df.duplicated().sum())
        ]
    })

    st.dataframe(
        info,
        use_container_width=True
    )

    st.divider()

    st.subheader("Column Details")
    column_profile = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Non Null": df.notnull().sum().values,
        "Null": df.isnull().sum().values,
        "Unique": df.nunique().values,
        "Missing %": ((df.isnull().sum() / len(df)) * 100).round(2).values
    })

    st.dataframe(
        column_profile,
        use_container_width=True
    )

    st.divider()

    st.subheader("Numeric Columns Summary")

    if numeric_cols:
        numeric_summary = df[numeric_cols].describe().T

        numeric_summary["Variance"] = df[numeric_cols].var()

        numeric_summary["Skewness"] = df[numeric_cols].skew()

        numeric_summary["Kurtosis"] = df[numeric_cols].kurt()

        st.dataframe(
            numeric_summary,
            use_container_width=True
        )
    else:
        st.info("No numeric columns found.")

    st.divider()

    st.subheader("Categorical Columns Summary")

    if categorical_cols:
        cat_summary = pd.DataFrame({
            "Column": categorical_cols,
            "Unique Values": [
                df[col].nunique()
                for col in categorical_cols
            ],
            "Most Frequent": [
                df[col].mode().iloc[0]
                if not df[col].mode().empty
                else ""
                for col in categorical_cols
            ],
            "Frequency": [
                df[col].value_counts().iloc[0]
                if not df[col].value_counts().empty
                else 0
                for col in categorical_cols
            ]
        })

        st.dataframe(
            cat_summary,
            use_container_width=True
        )
    else:
        st.info("No categorical columns found.")

    st.divider()

    st.subheader("Special Data Types")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Datetime Columns",
            len(datetime_cols)
        )

        if datetime_cols:
            st.write(datetime_cols)

    with c2:
        st.metric(
            "Boolean Columns",
            len(bool_cols)
        )

        if bool_cols:
            st.write(bool_cols)

    st.divider()
    st.subheader("Missing Value Analysis")

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isna().sum().values,
        "Missing %": (df.isna().sum() / len(df) * 100).round(2).values
    })

    st.dataframe(
        missing,
        use_container_width=True
    )

    st.divider()

    st.subheader("Memory Usage")

    memory = pd.DataFrame({
        "Column": df.columns,
        "Memory (KB)": (df.memory_usage(deep=True)[1:] / 1024).round(2).values
    })

    st.dataframe(
        memory,
        use_container_width=True
    )

    st.divider()

    st.subheader("Dataset Health")

    total_cells = rows * cols

    missing_cells = int(df.isna().sum().sum())

    duplicate_rows = int(df.duplicated().sum())

    health = max(
        0,
        round(
            (
                1 -
                (
                    (missing_cells / total_cells) * 0.7 +
                    (duplicate_rows / rows) * 0.3
                )
            ) * 100,
            2
        )
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Health Score",
        f"{health}%"
    )

    c2.metric(
        "Missing Cells",
        missing_cells
    )

    c3.metric(
        "Duplicate Rows",
        duplicate_rows
    )

    if health >= 90:
        st.success("Excellent dataset quality.")
    elif health >= 75:
        st.info("Good dataset quality.")
    elif health >= 50:
        st.warning("Dataset needs preprocessing.")
    else:
        st.error("Poor dataset quality.")

    st.divider()

    st.download_button(
        "📥 Download Dataset Profile",
        column_profile.to_csv(index=False).encode("utf-8"),
        file_name="dataset_profile.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.success("✅ Dataset profiling completed successfully.")