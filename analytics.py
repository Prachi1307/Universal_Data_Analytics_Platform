import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


def analytics_page():
    st.title("📈 Advanced Analytics")

    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("Please upload a dataset first.")
        return

    df = st.session_state.df.copy()

    if df.empty:
        st.warning("Dataset is empty.")
        return

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    st.subheader("Dataset Statistics")

    rows, cols = df.shape

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", rows)
    c2.metric("Columns", cols)
    c3.metric("Numeric", len(numeric_cols))
    c4.metric("Categorical", len(categorical_cols))

    st.divider()

    st.subheader("Descriptive Statistics")

    statistics = pd.DataFrame(index=numeric_cols)

    statistics["Mean"] = df[numeric_cols].mean()

    statistics["Median"] = df[numeric_cols].median()

    statistics["Mode"] = df[numeric_cols].mode().iloc[0]

    statistics["Minimum"] = df[numeric_cols].min()

    statistics["Maximum"] = df[numeric_cols].max()

    statistics["Range"] = (
        statistics["Maximum"] -
        statistics["Minimum"]
    )

    statistics["Variance"] = df[numeric_cols].var()

    statistics["Std Dev"] = df[numeric_cols].std()

    statistics["Skewness"] = df[numeric_cols].skew()

    statistics["Kurtosis"] = df[numeric_cols].kurt()

    st.dataframe(
        statistics.round(4),
        use_container_width=True
    )

    st.download_button(
        "📥 Download Statistics",
        statistics.to_csv().encode(),
        "statistics.csv",
        "text/csv",
        use_container_width=True
    )

    st.divider()

    st.subheader("Missing Values")

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing": df.isna().sum(),
        "Percentage": (
            df.isna().sum() / len(df) * 100
        ).round(2)
    })

    st.dataframe(
        missing,
        use_container_width=True
    )

    fig = px.bar(
        missing,
        x="Column",
        y="Missing",
        color="Missing",
        title="Missing Values",
        template="plotly"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Categorical Summary")

    if categorical_cols:
        column = st.selectbox(
            "Select Column",
            categorical_cols
        )

        freq = (
            df[column]
            .value_counts()
            .reset_index()
        )

        freq.columns = [
            column,
            "Count"
        ]

        freq["Percentage"] = (
            freq["Count"] /
            freq["Count"].sum() * 100
        ).round(2)

        st.dataframe(
            freq,
            use_container_width=True
        )

        fig = px.bar(
            freq,
            x=column,
            y="Count",
            color="Count",
            template="plotly"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No categorical columns found.")

    st.divider()

    st.subheader("Correlation Analysis")

    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr(numeric_only=True)

        st.dataframe(
            corr.round(3),
            use_container_width=True
        )

        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            aspect="auto",
            title="Correlation Heatmap"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        corr_pairs = (
            corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
            .stack()
            .reset_index()
        )

        corr_pairs.columns = [
            "Feature 1",
            "Feature 2",
            "Correlation"
        ]

        corr_pairs = corr_pairs.sort_values(
            by="Correlation",
            key=abs,
            ascending=False
        )

        st.subheader("Top Correlations")

        st.dataframe(
            corr_pairs.head(15),
            use_container_width=True
        )

    else:
        st.info("At least two numeric columns are required.")

    st.divider()

    st.subheader("Outlier Detection (IQR)")

    if numeric_cols:
        selected = st.selectbox(
            "Select Numeric Column",
            numeric_cols,
            key="outlier_column"
        )

        q1 = df[selected].quantile(0.25)

        q3 = df[selected].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        outliers = df[
            (df[selected] < lower) |
            (df[selected] > upper)
        ]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Outliers",
            len(outliers)
        )

        c2.metric(
            "Lower Limit",
            round(lower, 2)
        )

        c3.metric(
            "Upper Limit",
            round(upper, 2)
        )

        fig = px.box(
            df,
            y=selected,
            points="outliers",
            title=f"Outlier Detection - {selected}",
            template="plotly"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        if len(outliers):
            with st.expander("View Outliers"):
                st.dataframe(
                    outliers,
                    use_container_width=True
                )

    else:
        st.info("No numeric columns available.")

    st.divider()

    st.subheader("Group By Analysis")

    if numeric_cols and categorical_cols:
        group_col = st.selectbox(
            "Group By Column",
            categorical_cols
        )

        value_col = st.selectbox(
            "Numeric Column",
            numeric_cols
        )

        operation = st.selectbox(
            "Aggregation",
            [
                "Mean",
                "Sum",
                "Min",
                "Max",
                "Count",
                "Median"
            ]
        )

        if operation == "Mean":
            result = (
                df.groupby(group_col)[value_col]
                .mean()
                .reset_index()
            )

        elif operation == "Sum":
            result = (
                df.groupby(group_col)[value_col]
                .sum()
                .reset_index()
            )

        elif operation == "Min":
            result = (
                df.groupby(group_col)[value_col]
                .min()
                .reset_index()
            )

        elif operation == "Max":
            result = (
                df.groupby(group_col)[value_col]
                .max()
                .reset_index()
            )

        elif operation == "Median":
            result = (
                df.groupby(group_col)[value_col]
                .median()
                .reset_index()
            )

        else:
            result = (
                df.groupby(group_col)[value_col]
                .count()
                .reset_index()
            )

        st.dataframe(
            result,
            use_container_width=True
        )

        fig = px.bar(
            result,
            x=group_col,
            y=value_col,
            color=value_col,
            template="plotly"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("Group analysis requires numeric and categorical columns.")

    st.divider()

    st.subheader("Distribution Analysis")

    if numeric_cols:
        dist_col = st.selectbox(
            "Distribution Column",
            numeric_cols,
            key="distribution_column"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Skewness",
            round(df[dist_col].skew(), 4)
        )

        c2.metric(
            "Kurtosis",
            round(df[dist_col].kurt(), 4)
        )

        c3.metric(
            "Unique Values",
            df[dist_col].nunique()
        )

        fig = px.histogram(
            df,
            x=dist_col,
            marginal="box",
            nbins=30,
            template="plotly",
            title=f"Distribution of {dist_col}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("Data Quality Report")

    quality = pd.DataFrame({
        "Metric": [
            "Rows",
            "Columns",
            "Missing Values",
            "Duplicate Rows",
            "Numeric Columns",
            "Categorical Columns"
        ],
        "Value": [
            rows,
            cols,
            int(df.isna().sum().sum()),
            int(df.duplicated().sum()),
            len(numeric_cols),
            len(categorical_cols)
        ]
    })

    st.dataframe(
        quality,
        use_container_width=True
    )

    st.divider()

    st.subheader("AI Insights")

    insights = []

    insights.append(
        f"Dataset contains {rows:,} rows and {cols} columns."
    )

    if len(numeric_cols):
        insights.append(
            f"{len(numeric_cols)} numeric columns detected."
        )

    if len(categorical_cols):
        insights.append(
            f"{len(categorical_cols)} categorical columns detected."
        )

    missing_total = int(df.isna().sum().sum())

    if missing_total == 0:
        insights.append(
            "No missing values detected."
        )
    else:
        insights.append(
            f"{missing_total:,} missing values should be handled."
        )

    duplicate_total = int(df.duplicated().sum())

    if duplicate_total == 0:
        insights.append(
            "No duplicate rows detected."
        )
    else:
        insights.append(
            f"{duplicate_total} duplicate rows found."
        )

    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr().abs()

        np.fill_diagonal(corr.values, 0)

        highest = corr.stack().idxmax()

        value = corr.loc[highest]

        insights.append(
            f"Strongest correlation: {highest[0]} ↔ {highest[1]} ({value:.2f})"
        )

    if numeric_cols:
        outlier_counts = {}

        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)

            iqr = q3 - q1

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            count = (
                (df[col] < lower) |
                (df[col] > upper)
            ).sum()

            outlier_counts[col] = count

        worst = max(
            outlier_counts,
            key=outlier_counts.get
        )

        insights.append(
            f"Highest outliers detected in '{worst}' ({outlier_counts[worst]} values)."
        )

    for item in insights:
        st.success(item)

    st.divider()

    report = statistics.copy()

    report["Missing Values"] = df[numeric_cols].isna().sum()

    st.download_button(
        "📥 Download Analytics Report",
        report.to_csv().encode("utf-8"),
        file_name="analytics_report.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.success("✅ Analytics completed successfully.")