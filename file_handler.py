import pandas as pd
import streamlit as st


SUPPORTED_FILES = [
    "csv",
    "xlsx",
    "xls",
    "json",
    "parquet"
]


def load_dataset(uploaded_file):

    if uploaded_file is None:
        return None

    file_name = uploaded_file.name.lower()

    try:

        if file_name.endswith(".csv"):

            return pd.read_csv(uploaded_file)

        elif file_name.endswith(".xlsx"):

            return pd.read_excel(uploaded_file)

        elif file_name.endswith(".xls"):

            return pd.read_excel(uploaded_file)

        elif file_name.endswith(".json"):

            return pd.read_json(uploaded_file)

        elif file_name.endswith(".parquet"):

            return pd.read_parquet(uploaded_file)

        else:

            st.error("Unsupported File Type")
            return None

    except Exception as e:

        st.error(e)
        return None


def dataset_information(df):

    return {

        "Rows": df.shape[0],

        "Columns": df.shape[1],

        "Missing Values": int(df.isna().sum().sum()),

        "Duplicate Rows": int(df.duplicated().sum()),

        "Memory Usage (KB)": round(
            df.memory_usage(deep=True).sum()/1024,
            2
        )

    }


def column_information(df):

    return pd.DataFrame({

        "Column": df.columns,

        "Datatype": df.dtypes.astype(str),

        "Missing": df.isna().sum(),

        "Unique": df.nunique()

    })


def numeric_columns(df):

    return df.select_dtypes(include="number").columns.tolist()


def categorical_columns(df):

    return df.select_dtypes(exclude="number").columns.tolist()


def datetime_columns(df):

    return df.select_dtypes(
        include=["datetime64", "datetime64[ns]"]
    ).columns.tolist()


def object_columns(df):

    return df.select_dtypes(
        include="object"
    ).columns.tolist()


def clean_missing(df):

    return df.dropna()


def remove_duplicates(df):

    return df.drop_duplicates()


def save_session(df):

    st.session_state.df = df


def get_session():

    if "df" in st.session_state:
        return st.session_state.df

    return None