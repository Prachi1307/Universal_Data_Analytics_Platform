import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def dashboard_page():
    st.title("📊 Data Dashboard")
    st.markdown("Comprehensive overview of your uploaded dataset.")

    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("⚠ Please upload a dataset first.")
        return

    df = st.session_state.df.copy()

    if df.empty:
        st.warning("Dataset is empty.")
        return

    # -----------------------------
    # Dataset Information
    # -----------------------------
    rows, cols = df.shape

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    missing_values = int(df.isna().sum().sum())

    duplicate_rows = int(df.duplicated().sum())

    memory_usage = (
        df.memory_usage(deep=True).sum() / 1024
    )

    # -----------------------------
    # KPI Cards
    # -----------------------------
    st.subheader("📌 Dataset Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Rows",
        f"{rows:,}"
    )

    c2.metric(
        "Columns",
        cols
    )

    c3.metric(
        "Numeric",
        len(numeric_cols)
    )

    c4.metric(
        "Categorical",
        len(categorical_cols)
    )

    c5, c6, c7 = st.columns(3)

    c5.metric(
        "Missing Values",
        missing_values
    )

    c6.metric(
        "Duplicates",
        duplicate_rows
    )

    c7.metric(
        "Dataset Size",
        f"{memory_usage:.2f} KB"
    )

    st.divider()

    # -----------------------------
    # Preview
    # -----------------------------
    st.subheader("👀 Dataset Preview")

    preview_option = st.radio(
        "Select Preview",
        [
            "First 10 Rows",
            "Last 10 Rows",
            "Random Sample"
        ],
        horizontal=True
    )

    if preview_option == "First 10 Rows":
        st.dataframe(
            df.head(10),
            use_container_width=True
        )

    elif preview_option == "Last 10 Rows":
        st.dataframe(
            df.tail(10),
            use_container_width=True
        )

    else:
        sample_size = st.slider(
            "Sample Size",
            5,
            min(100, len(df)),
            10
        )

        st.dataframe(
            df.sample(sample_size),
            use_container_width=True
        )

    st.divider()

    # -----------------------------
    # Statistical Summary
    # -----------------------------
    st.subheader("📈 Statistical Summary")

    summary = df.describe(include="all").T

    st.dataframe(
        summary,
        use_container_width=True,
        height=450
    )

    csv_summary = summary.to_csv().encode("utf-8")

    st.download_button(
        "📥 Download Summary",
        csv_summary,
        "summary.csv",
        "text/csv",
        use_container_width=True
    )

    st.divider()

    # -----------------------------
    # Missing Value Analysis
    # -----------------------------
    st.subheader("❌ Missing Value Analysis")

    missing_df = (
        df.isnull()
        .sum()
        .reset_index()
    )

    missing_df.columns = [
        "Column",
        "Missing Values"
    ]

    missing_df["Percentage"] = (
        missing_df["Missing Values"] / len(df) * 100
    ).round(2)

    st.dataframe(
        missing_df,
        use_container_width=True
    )

    missing_chart = missing_df[
        missing_df["Missing Values"] > 0
    ]

    if not missing_chart.empty:
        fig = px.bar(
            missing_chart,
            x="Column",
            y="Missing Values",
            color="Missing Values",
            title="Missing Values by Column",
            template="plotly"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.success("✅ No missing values found.")

    st.divider()

    # -----------------------------
    # Data Type Analysis
    # -----------------------------
    st.subheader("🧬 Data Type Analysis")

    dtype_df = (
        df.dtypes
        .astype(str)
        .value_counts()
        .reset_index()
    )

    dtype_df.columns = [
        "Data Type",
        "Count"
    ]

    left, right = st.columns([1, 2])

    with left:
        st.dataframe(
            dtype_df,
            use_container_width=True
        )

    with right:
        fig = px.pie(
            dtype_df,
            names="Data Type",
            values="Count",
            hole=0.45,
            title="Column Data Types",
            template="plotly"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # -----------------------------
    # Numeric Columns
    # -----------------------------
    st.subheader("🔢 Numeric Columns")

    if numeric_cols:
        numeric_df = pd.DataFrame({
            "Numeric Columns": numeric_cols
        })

        st.dataframe(
            numeric_df,
            use_container_width=True
        )

    else:
        st.info("No numeric columns found.")

    st.divider()

    # -----------------------------
    # Categorical Columns
    # -----------------------------
    st.subheader("🏷️ Categorical Columns")

    if categorical_cols:
        categorical_df = pd.DataFrame({
            "Categorical Columns": categorical_cols
        })

        st.dataframe(
            categorical_df,
            use_container_width=True
        )

    else:
        st.info("No categorical columns found.")

    st.divider()

    # -----------------------------
    # Correlation Heatmap
    # -----------------------------
    st.subheader("🔥 Correlation Heatmap")

    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr(numeric_only=True)

        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            aspect="auto",
            title="Correlation Matrix"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("At least two numeric columns are required.")

    st.divider()

    # -----------------------------
    # Histogram Explorer
    # -----------------------------
    st.subheader("📊 Histogram Explorer")

    if numeric_cols:
        selected_col = st.selectbox(
            "Select Numeric Column",
            numeric_cols
        )

        bins = st.slider(
            "Number of Bins",
            min_value=5,
            max_value=100,
            value=30
        )

        fig = px.histogram(
            df,
            x=selected_col,
            nbins=bins,
            title=f"Distribution of {selected_col}",
            template="plotly"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No numeric columns available.")

    st.divider()

    # -----------------------------
    # Box Plot
    # -----------------------------
    st.subheader("📦 Box Plot")

    if numeric_cols:
        box_col = st.selectbox(
            "Box Plot Column",
            numeric_cols,
            key="box_plot_column"
        )

        fig = px.box(
            df,
            y=box_col,
            points="outliers",
            title=f"Box Plot - {box_col}",
            template="plotly"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # -----------------------------
    # Value Counts
    # -----------------------------
    st.subheader("📈 Category Distribution")

    if categorical_cols:
        cat_col = st.selectbox(
            "Categorical Column",
            categorical_cols
        )

        value_counts = (
            df[cat_col]
            .astype(str)
            .value_counts()
            .reset_index()
        )

        value_counts.columns = [
            cat_col,
            "Count"
        ]

        fig = px.bar(
            value_counts,
            x=cat_col,
            y="Count",
            color="Count",
            title=f"{cat_col} Distribution",
            template="plotly"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info("No categorical columns available.")

    st.divider()

    # -----------------------------
    # Dataset Health
    # -----------------------------
    st.subheader("🎯 Dataset Health")

    score = 100

    score -= min(
        30,
        (missing_values / max(rows * cols, 1)) * 100
    )

    score -= min(
        20,
        (duplicate_rows / max(rows, 1)) * 100
    )

    score = max(0, round(score))

    if score >= 90:
        st.success(f"Excellent Dataset Quality ({score}/100)")
    elif score >= 75:
        st.info(f"Good Dataset Quality ({score}/100)")
    elif score >= 50:
        st.warning(f"Average Dataset Quality ({score}/100)")
    else:
        st.error(f"Poor Dataset Quality ({score}/100)")

    st.divider()

    # -----------------------------
    # Quick Insights
    # -----------------------------
    st.subheader("🤖 Quick Insights")

    insights = []

    insights.append(f"• Dataset contains **{rows:,} rows** and **{cols} columns**.")
    insights.append(f"• Numeric columns: **{len(numeric_cols)}**.")
    insights.append(f"• Categorical columns: **{len(categorical_cols)}**.")
    insights.append(f"• Missing values: **{missing_values:,}**.")
    insights.append(f"• Duplicate rows: **{duplicate_rows:,}**.")

    if missing_values == 0:
        insights.append("• No missing values detected.")
    else:
        insights.append("• Consider handling missing values before analysis.")

    if duplicate_rows > 0:
        insights.append("• Remove duplicate rows for better model accuracy.")

    if len(numeric_cols) >= 2:
        insights.append("• Dataset is suitable for correlation analysis.")

    if len(numeric_cols) >= 3:
        insights.append("• Dataset is suitable for Machine Learning.")

    for item in insights:
        st.markdown(item)

    st.divider()

    st.success("✅ Dashboard generated successfully.")