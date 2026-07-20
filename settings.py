import streamlit as st


def settings_page():
    st.title("⚙️ Settings")

    st.subheader("Application Settings")

    theme = st.selectbox(
        "Theme",
        ["Light", "Dark"]
    )

    page_size = st.slider(
        "Rows to Display",
        10,
        500,
        100
    )

    chart_theme = st.selectbox(
        "Chart Template",
        [
            "plotly",
            "plotly_white",
            "plotly_dark",
            "ggplot2",
            "seaborn"
        ]
    )

    auto_refresh = st.checkbox(
        "Enable Auto Refresh",
        value=False
    )

    show_grid = st.checkbox(
        "Show Chart Grid",
        value=True
    )

    animation = st.checkbox(
        "Enable Chart Animation",
        value=True
    )

    st.divider()

    st.subheader("Export Settings")

    default_export = st.selectbox(
        "Default Export Format",
        [
            "CSV",
            "Excel",
            "PDF"
        ]
    )

    include_index = st.checkbox(
        "Include DataFrame Index",
        value=False
    )

    compression = st.selectbox(
        "Compression",
        [
            "None",
            "ZIP"
        ]
    )

    st.divider()
    st.subheader("Session Settings")

    clear_session = st.button(
        "🗑 Clear Session Data",
        use_container_width=True
    )

    reset_settings = st.button(
        "🔄 Reset Settings",
        use_container_width=True
    )

    if clear_session:
        keys = list(st.session_state.keys())

        for key in keys:
            del st.session_state[key]

        st.success("Session cleared successfully.")

    if reset_settings:
        st.session_state["theme"] = "Light"
        st.session_state["page_size"] = 100
        st.session_state["chart_theme"] = "plotly"
        st.session_state["default_export"] = "CSV"

        st.success("Settings reset successfully.")

    st.divider()

    st.subheader("Current Configuration")

    settings = {
        "Theme": theme,
        "Rows per Page": page_size,
        "Chart Template": chart_theme,
        "Auto Refresh": auto_refresh,
        "Show Grid": show_grid,
        "Chart Animation": animation,
        "Default Export": default_export,
        "Include Index": include_index,
        "Compression": compression
    }

    st.json(settings)

    if st.button(
        "💾 Save Settings",
        use_container_width=True
    ):
        st.session_state["theme"] = theme
        st.session_state["page_size"] = page_size
        st.session_state["chart_theme"] = chart_theme
        st.session_state["auto_refresh"] = auto_refresh
        st.session_state["show_grid"] = show_grid
        st.session_state["animation"] = animation
        st.session_state["default_export"] = default_export
        st.session_state["include_index"] = include_index
        st.session_state["compression"] = compression

        st.success("✅ Settings saved successfully.")

    st.divider()

    st.subheader("About")

    st.info("""
**Universal Data Analytics Platform**

Version : 1.0

Developed using:
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-Learn
- ReportLab

Features:
- Data Upload
- Data Cleaning
- Dashboard
- Visualization
- Analytics
- Machine Learning
- Report Generation
- Dataset Profiling
""")

    st.success("✅ Settings module loaded successfully.")