import pandas as pd
import numpy as np
from sklearn.preprocessing import (
    LabelEncoder,
    StandardScaler,
    MinMaxScaler,
    RobustScaler
)
from sklearn.impute import SimpleImputer


def split_columns(df):

    numerical = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical = df.select_dtypes(
        exclude=np.number
    ).columns.tolist()

    return numerical, categorical


def remove_duplicates(df):

    return df.drop_duplicates()


def remove_missing(df):

    return df.dropna()


def fill_missing(df, strategy="mean"):

    df = df.copy()

    num_cols = df.select_dtypes(
        include=np.number
    ).columns

    cat_cols = df.select_dtypes(
        exclude=np.number
    ).columns

    if len(num_cols):

        imp = SimpleImputer(strategy=strategy)

        df[num_cols] = imp.fit_transform(
            df[num_cols]
        )

    if len(cat_cols):

        imp = SimpleImputer(
            strategy="most_frequent"
        )

        df[cat_cols] = imp.fit_transform(
            df[cat_cols]
        )

    return df


def label_encode(df):

    df = df.copy()

    encoders = {}

    for col in df.select_dtypes(
        exclude=np.number
    ).columns:

        le = LabelEncoder()

        df[col] = le.fit_transform(
            df[col].astype(str)
        )

        encoders[col] = le

    return df, encoders


def one_hot_encode(df):

    return pd.get_dummies(
        df,
        drop_first=True
    )


def standard_scale(df):

    scaler = StandardScaler()

    numeric = df.select_dtypes(
        include=np.number
    ).columns

    df = df.copy()

    df[numeric] = scaler.fit_transform(
        df[numeric]
    )

    return df, scaler


def minmax_scale(df):

    scaler = MinMaxScaler()

    numeric = df.select_dtypes(
        include=np.number
    ).columns

    df = df.copy()

    df[numeric] = scaler.fit_transform(
        df[numeric]
    )

    return df, scaler


def robust_scale(df):

    scaler = RobustScaler()

    numeric = df.select_dtypes(
        include=np.number
    ).columns

    df = df.copy()

    df[numeric] = scaler.fit_transform(
        df[numeric]
    )

    return df, scaler


def detect_outliers_iqr(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    outliers = {}

    for col in numeric.columns:

        q1 = numeric[col].quantile(0.25)

        q3 = numeric[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        outliers[col] = df[
            (df[col] < lower) |
            (df[col] > upper)
        ].index.tolist()

    return outliers


def remove_outliers_iqr(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    cleaned = df.copy()

    for col in numeric.columns:

        q1 = cleaned[col].quantile(0.25)

        q3 = cleaned[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        cleaned = cleaned[
            (cleaned[col] >= lower) &
            (cleaned[col] <= upper)
        ]

    return cleaned


def normalize_text(df):

    df = df.copy()

    for col in df.select_dtypes(
        include="object"
    ).columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    return df


def preprocess_pipeline(df):

    df = remove_duplicates(df)

    df = fill_missing(df)

    df = normalize_text(df)

    df, _ = label_encode(df)

    return df