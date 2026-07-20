import streamlit as st

# ==============================
# Page Configuration (MUST BE FIRST)
# ==============================
st.set_page_config(
    page_title="Universal Data Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Import Modules
# ==============================
from modules.home import home_page
from modules.upload import upload_page
from modules.preview import preview_page
from modules.dashboard import dashboard_page
from modules.visualization import visualization_page
from modules.analytics import analytics_page
from modules.machine_learning import machine_learning_page
from modules.reports import reports_page
from modules.profile import profile_page
from modules.settings import settings_page

# ==============================
# Load Custom CSS
# ==============================
def load_css():
    try:
        with open("assets/style.css", "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except Exception:
        pass


load_css()

# ==============================
# Session State Initialization
# ==============================
defaults = {
    "page": "🏠 Home",
    "df": None,
    "theme": "Light",
    "page_size": 100,
    "chart_theme": "plotly",
    "default_export": "CSV"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ==============================
# Header
# ==============================
st.markdown(
    """
    <div style='text-align:center;padding:15px'>
        <h1>📊 Universal Data Analytics Platform</h1>
        <h5>Upload • Analyze • Visualize • Machine Learning • Reports</h5>
    </div>
    """,
    unsafe_allow_html=True
)

# ==============================
# Sidebar Navigation
# ==============================
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "",
    [
        "🏠 Home",
        "📁 Upload",
        "👀 Preview",
        "📊 Dashboard",
        "📈 Visualization",
        "📉 Analytics",
        "🤖 Machine Learning",
        "📄 Reports",
        "👤 Profile",
        "⚙️ Settings"
    ],
    index=[
        "🏠 Home",
        "📁 Upload",
        "👀 Preview",
        "📊 Dashboard",
        "📈 Visualization",
        "📉 Analytics",
        "🤖 Machine Learning",
        "📄 Reports",
        "👤 Profile",
        "⚙️ Settings"
    ].index(st.session_state.page)
)

st.session_state.page = page

# ==============================
# Sidebar Dataset Info
# ==============================
st.sidebar.markdown("---")

if st.session_state.df is not None:

    df = st.session_state.df

    st.sidebar.success("Dataset Loaded")

    st.sidebar.metric(
        "Rows",
        df.shape[0]
    )

    st.sidebar.metric(
        "Columns",
        df.shape[1]
    )

    st.sidebar.metric(
        "Missing",
        int(df.isna().sum().sum())
    )

else:

    st.sidebar.warning("No Dataset Loaded")

st.sidebar.markdown("---")
st.sidebar.caption("Universal Data Analytics Platform v1.0")

# ==============================
# Page Routing
# ==============================
try:

    if page == "🏠 Home":
        home_page()

    elif page == "📁 Upload":
        upload_page()

    elif page == "👀 Preview":
        preview_page()

    elif page == "📊 Dashboard":
        dashboard_page()

    elif page == "📈 Visualization":
        visualization_page()

    elif page == "📉 Analytics":
        analytics_page()

    elif page == "🤖 Machine Learning":
        machine_learning_page()

    elif page == "📄 Reports":
        reports_page()

    elif page == "👤 Profile":
        profile_page()

    elif page == "⚙️ Settings":
        settings_page()

except Exception as e:

    st.error("An unexpected error occurred.")

    with st.expander("Error Details"):
        st.exception(e)