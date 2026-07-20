import pandas as pd
from io import BytesIO


def export_csv(df):
    return df.to_csv(index=False).encode("utf-8")


def export_excel(df, sheet_name="Dataset"):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name=sheet_name
        )

    output.seek(0)

    return output.getvalue()


def export_json(df):

    return df.to_json(
        orient="records",
        indent=4
    )


def export_html(df):

    return df.to_html(
        index=False,
        border=0
    )


def export_markdown(df):

    return df.to_markdown(
        index=False
    )


def dataset_summary(df):

    return {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": int(df.isna().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Memory (MB)": round(
            df.memory_usage(deep=True).sum() /
            (1024 * 1024),
            2
        )
    }


def numeric_summary(df):

    return df.describe().round(2)


def categorical_summary(df):

    cat = df.select_dtypes(
        exclude="number"
    )

    if cat.empty:
        return pd.DataFrame()

    return pd.DataFrame({
        "Unique Values": cat.nunique(),
        "Missing": cat.isna().sum(),
        "Most Frequent": cat.mode().iloc[0]
    })


def missing_value_report(df):

    report = pd.DataFrame({
        "Column": df.columns,
        "Missing": df.isna().sum().values,
        "Percentage": (
            df.isna().sum() /
            len(df) * 100
        ).round(2).values
    })

    return report


def data_type_report(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values
    })