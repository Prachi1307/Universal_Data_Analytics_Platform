import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from io import BytesIO


# ==========================================================
# Visualization Page
# ==========================================================

def visualization_page():
    st.title("📊 Data Visualization")

    # ------------------------------------------------------
    # Check Dataset
    # ------------------------------------------------------

    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("Please upload a dataset first.")
        return

    df = st.session_state.df.copy()

    if df.empty:
        st.warning("Dataset is empty.")
        return

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()
    all_cols = df.columns.tolist()

    if len(all_cols) == 0:
        st.warning("Dataset has no columns.")
        return

    # ------------------------------------------------------
    # Visualization Controls
    # ------------------------------------------------------

    st.sidebar.header("Visualization Settings")

    chart_type = st.sidebar.selectbox(
        "Chart Type",
        [
            "Bar",
            "Line",
            "Scatter",
            "Bubble",
            "Histogram",
            "Box",
            "Pie",
            "Heatmap",
            "Violin",
            "3D Scatter"
        ],
        key="chart_type"
    )

    title = st.sidebar.text_input(
        "Chart Title",
        value=f"{chart_type} Chart",
        key="chart_title"
    )

    theme = st.sidebar.selectbox(
        "Chart Theme",
        [
            "plotly",
            "plotly_white",
            "plotly_dark",
            "ggplot2",
            "seaborn"
        ],
        key="chart_theme"
    )

    color = st.sidebar.selectbox(
        "Color By (Optional)",
        ["None"] + all_cols,
        key="color_column"
    )

    # ------------------------------------------------------
    # Row Filter
    # ------------------------------------------------------

    max_rows = len(df)

    row_range = st.sidebar.slider(
        "Filter Rows",
        min_value=0,
        max_value=max_rows,
        value=(0, max_rows),
        key="row_filter"
    )

    filtered_df = df.iloc[row_range[0]:row_range[1]].copy()

    if filtered_df.empty:
        st.warning("No rows available after filtering.")
        return

    fig = None

    # =====================================================
    # BAR CHART
    # =====================================================

    if chart_type == "Bar":
        x = st.sidebar.selectbox(
            "X Axis",
            all_cols,
            key="bar_x"
        )

        y = st.sidebar.selectbox(
            "Y Axis",
            numeric_cols,
            key="bar_y"
        )

        fig = px.bar(
            filtered_df,
            x=x,
            y=y,
            color=None if color == "None" else color,
            template=theme,
            title=title
        )

    # =====================================================
    # LINE CHART
    # =====================================================

    elif chart_type == "Line":
        x = st.sidebar.selectbox(
            "X Axis",
            all_cols,
            key="line_x"
        )

        y = st.sidebar.selectbox(
            "Y Axis",
            numeric_cols,
            key="line_y"
        )

        fig = px.line(
            filtered_df,
            x=x,
            y=y,
            color=None if color == "None" else color,
            markers=True,
            template=theme,
            title=title
        )

    # =====================================================
    # SCATTER CHART
    # =====================================================

    elif chart_type == "Scatter":
        if len(numeric_cols) < 2:
            st.warning("Scatter Plot requires at least two numeric columns.")
            return

        x = st.sidebar.selectbox(
            "X Axis",
            numeric_cols,
            key="scatter_x"
        )

        y = st.sidebar.selectbox(
            "Y Axis",
            numeric_cols,
            index=1,
            key="scatter_y"
        )

        fig = px.scatter(
            filtered_df,
            x=x,
            y=y,
            color=None if color == "None" else color,
            template=theme,
            title=title
        )

    # =====================================================
    # BUBBLE CHART
    # =====================================================

    elif chart_type == "Bubble":
        if len(numeric_cols) < 3:
            st.warning("Bubble Chart requires at least three numeric columns.")
            return

        x = st.sidebar.selectbox(
            "X Axis",
            numeric_cols,
            key="bubble_x"
        )

        y_options = [c for c in numeric_cols if c != x]

        y = st.sidebar.selectbox(
            "Y Axis",
            y_options,
            key="bubble_y"
        )

        size_options = [c for c in y_options if c != y]

        size = st.sidebar.selectbox(
            "Bubble Size",
            size_options,
            key="bubble_size"
        )

        fig = px.scatter(
            filtered_df,
            x=x,
            y=y,
            size=size,
            color=None if color == "None" else color,
            template=theme,
            title=title
        )

    # =====================================================
    # HISTOGRAM
    # =====================================================

    elif chart_type == "Histogram":
        if len(numeric_cols) == 0:
            st.warning("Histogram requires at least one numeric column.")
            return

        x = st.sidebar.selectbox(
            "Column",
            numeric_cols,
            key="hist_x"
        )

        bins = st.sidebar.slider(
            "Number of Bins",
            min_value=5,
            max_value=100,
            value=30,
            key="hist_bins"
        )

        fig = px.histogram(
            filtered_df,
            x=x,
            nbins=bins,
            color=None if color == "None" else color,
            template=theme,
            title=title
        )

    # =====================================================
    # BOX PLOT
    # =====================================================

    elif chart_type == "Box":
        if len(numeric_cols) == 0:
            st.warning("Box Plot requires at least one numeric column.")
            return

        category = st.sidebar.selectbox(
            "Category (Optional)",
            ["None"] + categorical_cols,
            key="box_category"
        )

        value = st.sidebar.selectbox(
            "Numeric Column",
            numeric_cols,
            key="box_value"
        )

        fig = px.box(
            filtered_df,
            x=None if category == "None" else category,
            y=value,
            color=None if color == "None" else color,
            template=theme,
            title=title
        )

    # =====================================================
    # PIE CHART
    # =====================================================

    elif chart_type == "Pie":
        if len(categorical_cols) == 0:
            st.warning("Pie Chart requires at least one categorical column.")
            return

        if len(numeric_cols) == 0:
            st.warning("Pie Chart requires at least one numeric column.")
            return

        names = st.sidebar.selectbox(
            "Category",
            categorical_cols,
            key="pie_category"
        )

        values = st.sidebar.selectbox(
            "Values",
            numeric_cols,
            key="pie_values"
        )

        pie_df = (
            filtered_df
            .groupby(names, dropna=False)[values]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            pie_df,
            names=names,
            values=values,
            hole=0.35,
            template=theme,
            title=title
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

    # =====================================================
    # HEATMAP
    # =====================================================

    elif chart_type == "Heatmap":
        if len(numeric_cols) < 2:
            st.warning("Heatmap requires at least two numeric columns.")
            return

        corr = filtered_df[numeric_cols].corr(numeric_only=True)

        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="RdBu_r",
            template=theme,
            title=title
        )

    # =====================================================
    # VIOLIN PLOT
    # =====================================================

    elif chart_type == "Violin":
        if len(numeric_cols) == 0:
            st.warning("Violin Plot requires at least one numeric column.")
            return

        if len(categorical_cols) == 0:
            st.warning("Violin Plot requires at least one categorical column.")
            return

        x = st.sidebar.selectbox(
            "Category",
            categorical_cols,
            key="violin_x"
        )

        y = st.sidebar.selectbox(
            "Numeric Column",
            numeric_cols,
            key="violin_y"
        )

        fig = px.violin(
            filtered_df,
            x=x,
            y=y,
            color=None if color == "None" else color,
            box=True,
            points="all",
            template=theme,
            title=title
        )

    # =====================================================
    # 3D SCATTER
    # =====================================================

    elif chart_type == "3D Scatter":
        if len(numeric_cols) < 3:
            st.warning("3D Scatter requires at least three numeric columns.")
            return

        x = st.sidebar.selectbox(
            "X Axis",
            numeric_cols,
            key="scatter3d_x"
        )

        remaining_y = [c for c in numeric_cols if c != x]

        y = st.sidebar.selectbox(
            "Y Axis",
            remaining_y,
            key="scatter3d_y"
        )

        remaining_z = [c for c in remaining_y if c != y]

        z = st.sidebar.selectbox(
            "Z Axis",
            remaining_z,
            key="scatter3d_z"
        )

        fig = px.scatter_3d(
            filtered_df,
            x=x,
            y=y,
            z=z,
            color=None if color == "None" else color,
            template=theme,
            title=title
        )

        fig.update_traces(
            marker=dict(size=6)
        )

    # =====================================================
    # DISPLAY CHART
    # =====================================================

    if fig is not None:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Chart Settings")

        chart_height = st.sidebar.slider(
            "Chart Height",
            min_value=400,
            max_value=900,
            value=600,
            key="chart_height"
        )

        show_grid = st.sidebar.checkbox(
            "Show Grid",
            value=True,
            key="show_grid"
        )

        show_legend = st.sidebar.checkbox(
            "Show Legend",
            value=True,
            key="show_legend"
        )

        fig.update_layout(
            height=chart_height,
            template=theme,
            showlegend=show_legend,
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        fig.update_xaxes(showgrid=show_grid)
        fig.update_yaxes(showgrid=show_grid)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # =====================================================
        # DATA PREVIEW
        # =====================================================

        with st.expander("📄 View Filtered Dataset"):
            st.dataframe(
                filtered_df,
                use_container_width=True
            )

        # =====================================================
        # SUMMARY
        # =====================================================

        st.markdown("### Dataset Summary")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Rows",
            filtered_df.shape[0]
        )

        c2.metric(
            "Columns",
            filtered_df.shape[1]
        )

        c3.metric(
            "Missing Values",
            int(filtered_df.isna().sum().sum())
        )

        # =====================================================
        # DOWNLOAD DATA
        # =====================================================

        csv = filtered_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Filtered Dataset",
            data=csv,
            file_name="filtered_dataset.csv",
            mime="text/csv",
            use_container_width=True
        )

        # =====================================================
        # DOWNLOAD CHART
        # =====================================================

        html = fig.to_html(include_plotlyjs="cdn").encode("utf-8")

        st.download_button(
            label="📊 Download Chart (HTML)",
            data=html,
            file_name="chart.html",
            mime="text/html",
            use_container_width=True
        )

    else:
        st.info("Please configure the chart options.")