import pandas as pd
import numpy as np


def get_numeric_columns(df):

    return df.select_dtypes(
        include=np.number
    ).columns.tolist()


def get_categorical_columns(df):

    return df.select_dtypes(
        exclude=np.number
    ).columns.tolist()


def dataset_info(df):

    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": int(df.isna().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Memory Usage (MB)": round(
            df.memory_usage(deep=True).sum() /
            (1024 ** 2),
            2
        )
    }


def missing_report(df):

    report = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isna().sum().values,
        "Missing %": (
            df.isna().sum() /
            len(df) * 100
        ).round(2).values
    })

    return report


def duplicate_report(df):

    return df[df.duplicated()].copy()


def remove_duplicates(df):

    return df.drop_duplicates().copy()


def remove_missing(df):

    return df.dropna().copy()


def fill_numeric(df):

    new_df = df.copy()

    numeric = get_numeric_columns(new_df)

    for col in numeric:

        new_df[col] = new_df[col].fillna(
            new_df[col].mean()
        )

    return new_df


def fill_categorical(df):

    new_df = df.copy()

    categorical = get_categorical_columns(new_df)

    for col in categorical:

        mode = new_df[col].mode()

        if not mode.empty:

            new_df[col] = new_df[col].fillna(
                mode.iloc[0]
            )

    return new_df


def memory_usage(df):

    return round(
        df.memory_usage(deep=True).sum() /
        (1024 ** 2),
        2
    )


def health_score(df):

    total = df.shape[0] * df.shape[1]

    missing = df.isna().sum().sum()

    duplicates = df.duplicated().sum()

    if total == 0:

        return 0

    score = (
        1 -
        (
            (missing / total) * 0.7 +
            (duplicates / max(df.shape[0], 1)) * 0.3
        )
    ) * 100

    return round(
        max(0, score),
        2
    )


def file_size_mb(file):

    return round(
        len(file.getvalue()) /
        (1024 * 1024),
        2
    )


def dataframe_preview(df, rows=10):

    return df.head(rows)


def dataframe_tail(df, rows=10):

    return df.tail(rows)


def dataframe_sample(df, rows=10):

    rows = min(rows, len(df))

    return df.sample(
        rows,
        random_state=42
    )


def unique_summary(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Unique Values": df.nunique().values
    })


def datatype_summary(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values
    })


def correlation_matrix(df):

    numeric = get_numeric_columns(df)

    if len(numeric) < 2:

        return pd.DataFrame()

    return df[numeric].corr()


def statistics(df):

    return df.describe(
        include="all"
    ).fillna("")


def is_dataset_loaded():

    try:
        import streamlit as st

        return "df" in st.session_state

    except Exception:

        return False