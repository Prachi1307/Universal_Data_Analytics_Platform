import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_pdf(df):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Universal Data Analytics Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    info = [
        ["Rows", str(df.shape[0])],
        ["Columns", str(df.shape[1])],
        ["Missing Values", str(df.isna().sum().sum())],
        ["Duplicate Rows", str(df.duplicated().sum())]
    ]

    table = Table(info)

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10)
        ])
    )

    elements.append(table)

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Statistical Summary",
            styles["Heading2"]
        )
    )

    summary = df.describe(include="all").fillna("").reset_index()

    summary_data = [summary.columns.tolist()] + summary.values.tolist()

    summary_table = Table(summary_data)

    summary_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
            ("FONTSIZE", (0, 0), (-1, -1), 8)
        ])
    )

    elements.append(summary_table)

    doc.build(elements)

    buffer.seek(0)

    return buffer


def reports_page():
    st.title("📑 Reports")

    if "df" not in st.session_state:
        st.warning("Upload dataset first.")
        return

    df = st.session_state.df.copy()

    if df.empty:
        st.warning("Dataset is empty.")
        return

    st.subheader("Dataset Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing", int(df.isna().sum().sum()))
    c4.metric("Duplicates", int(df.duplicated().sum()))

    st.divider()
    st.subheader("Statistical Summary")

    summary = df.describe(include="all").fillna("")

    st.dataframe(
        summary,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Statistics (CSV)",
        summary.to_csv().encode("utf-8"),
        file_name="statistics.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()

    st.subheader("Missing Values Report")

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isna().sum().values,
        "Percentage": (
            df.isna().sum() / len(df) * 100
        ).round(2).values
    })

    st.dataframe(
        missing,
        use_container_width=True
    )

    fig = px.bar(
        missing,
        x="Column",
        y="Missing Values",
        color="Missing Values",
        title="Missing Values Report"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Data Types")

    dtype_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(
        dtype_df,
        use_container_width=True
    )

    st.download_button(
        "📥 Download Data Types",
        dtype_df.to_csv(index=False).encode("utf-8"),
        file_name="data_types.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()

    st.subheader("Duplicate Records")

    duplicates = df[df.duplicated()]

    st.metric(
        "Duplicate Rows",
        len(duplicates)
    )

    if not duplicates.empty:
        st.dataframe(
            duplicates,
            use_container_width=True
        )
    else:
        st.success("No duplicate rows found.")

    st.divider()
    st.subheader("Correlation Report")

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] >= 2:
        corr = numeric_df.corr()

        st.dataframe(
            corr,
            use_container_width=True
        )

        fig = px.imshow(
            corr,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            title="Correlation Matrix"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    else:
        st.info("Not enough numeric columns for correlation analysis.")

    st.divider()

    st.subheader("Dataset Preview")

    rows = st.slider(
        "Rows to Preview",
        5,
        100,
        10
    )

    st.dataframe(
        df.head(rows),
        use_container_width=True
    )

    st.divider()

    st.subheader("Download Reports")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Dataset (CSV)",
        csv,
        file_name="dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

    excel = BytesIO()

    with pd.ExcelWriter(excel, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Dataset"
        )

        summary.to_excel(
            writer,
            sheet_name="Statistics"
        )

        missing.to_excel(
            writer,
            index=False,
            sheet_name="Missing Values"
        )

        dtype_df.to_excel(
            writer,
            index=False,
            sheet_name="Data Types"
        )

    st.download_button(
        "📊 Download Excel Report",
        excel.getvalue(),
        file_name="analytics_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    pdf = generate_pdf(df)

    st.download_button(
        "📄 Download PDF Report",
        pdf,
        file_name="analytics_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.success("✅ Reports generated successfully.")