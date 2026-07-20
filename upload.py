import streamlit as st
import pandas as pd


SUPPORTED_FILES = [
    "csv",
    "xlsx",
    "xls",
    "json",
    "parquet"
]


def detect_datetime(df):

    for col in df.columns:

        if df[col].dtype == "object":

            try:

                converted = pd.to_datetime(df[col])

                if converted.notna().sum() > len(df) * 0.8:

                    df[col] = converted

            except:
                pass

    return df


def upload_page():

    st.title("📁 Upload Dataset")

    st.write(
        "Upload any CSV, Excel, JSON or Parquet dataset."
    )

    uploaded = st.file_uploader(

        "Choose Dataset",

        type=SUPPORTED_FILES,

        accept_multiple_files=False

    )

    if uploaded is None:

        st.info("Waiting for dataset...")

        return

    extension = uploaded.name.split(".")[-1].lower()

    try:

        with st.spinner("Reading Dataset..."):

            if extension == "csv":

                df = pd.read_csv(uploaded)

            elif extension in ["xlsx", "xls"]:

                df = pd.read_excel(uploaded)

            elif extension == "json":

                df = pd.read_json(uploaded)

            elif extension == "parquet":

                df = pd.read_parquet(uploaded)

            else:

                st.error("Unsupported File")

                return

        df.columns = [

            str(col).strip()

            for col in df.columns

        ]

        df = detect_datetime(df)

        st.session_state.df = df

        st.success("Dataset Imported Successfully")

    except Exception as e:

        st.error(e)

        return

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", len(df))

    c2.metric("Columns", len(df.columns))

    c3.metric(
        "Missing Values",
        int(df.isna().sum().sum())
    )

    c4.metric(
        "Duplicate Rows",
        int(df.duplicated().sum())
    )

    st.divider()

    st.subheader("Dataset Preview")

    rows = st.slider(

        "Rows to Preview",

        5,

        min(100, len(df)),

        10

    )

    st.dataframe(

        df.head(rows),

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    st.subheader("Column Summary")

    summary = pd.DataFrame({

        "Column": df.columns,

        "Datatype": df.dtypes.astype(str),

        "Missing": df.isna().sum().values,

        "Unique": df.nunique().values

    })

    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    st.subheader("Detected Columns")

    numeric = df.select_dtypes(

        include="number"

    ).columns.tolist()

    categorical = df.select_dtypes(

        include=["object", "category"]

    ).columns.tolist()

    datetime_cols = df.select_dtypes(

        include=["datetime64", "datetime64[ns]"]

    ).columns.tolist()

    boolean = df.select_dtypes(

        include="bool"

    ).columns.tolist()

    a, b = st.columns(2)

    with a:

        st.write("### 🔢 Numeric")

        st.write(numeric if numeric else "None")

        st.write("")

        st.write("### 📅 Date")

        st.write(datetime_cols if datetime_cols else "None")

    with b:

        st.write("### 📝 Categorical")

        st.write(categorical if categorical else "None")

        st.write("")

        st.write("### ☑ Boolean")

        st.write(boolean if boolean else "None")

    st.divider()

    st.download_button(

        "⬇ Download Clean Dataset",

        df.to_csv(index=False).encode(),

        file_name="clean_dataset.csv",

        mime="text/csv",

        use_container_width=True

    )