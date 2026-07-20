import streamlit as st
import pandas as pd


def preview_page():

    st.title("🔍 Dataset Explorer")

    if st.session_state.df is None:

        st.warning("Please upload a dataset first.")

        return

    df = st.session_state.df.copy()

    st.sidebar.empty()

    st.subheader("Dataset Information")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))
    c3.metric("Memory", f"{df.memory_usage(deep=True).sum()/1024/1024:.2f} MB")
    c4.metric("Duplicates", int(df.duplicated().sum()))

    st.divider()

    left, right = st.columns([2, 1])

    with left:

        selected_columns = st.multiselect(

            "Select Columns",

            df.columns.tolist(),

            default=df.columns.tolist()

        )

    with right:

        max_rows = st.number_input(

            "Rows",

            min_value=5,

            max_value=len(df),

            value=min(100, len(df))

        )

    df = df[selected_columns]

    st.divider()

    st.subheader("Search")

    keyword = st.text_input("Search Entire Dataset")

    if keyword:

        mask = df.astype(str).apply(

            lambda x: x.str.contains(

                keyword,

                case=False,

                na=False

            )

        ).any(axis=1)

        df = df[mask]

    st.divider()

    st.subheader("Column Filters")

    filter_columns = st.multiselect(

        "Choose Columns to Filter",

        df.columns

    )

    for col in filter_columns:

        if pd.api.types.is_numeric_dtype(df[col]):

            minimum = float(df[col].min())

            maximum = float(df[col].max())

            value = st.slider(

                col,

                minimum,

                maximum,

                (minimum, maximum)

            )

            df = df[

                (df[col] >= value[0]) &

                (df[col] <= value[1])

            ]

        else:

            values = st.multiselect(

                col,

                sorted(df[col].dropna().unique()),

                default=sorted(df[col].dropna().unique())

            )

            df = df[df[col].isin(values)]

    st.divider()

    st.subheader("Sorting")

    c1, c2 = st.columns(2)

    with c1:

        sort_column = st.selectbox(

            "Sort Column",

            ["None"] + df.columns.tolist()

        )

    with c2:

        order = st.radio(

            "Order",

            ["Ascending", "Descending"],

            horizontal=True

        )

    if sort_column != "None":

        df = df.sort_values(

            sort_column,

            ascending=order == "Ascending"

        )

    st.divider()

    st.subheader("Preview")

    st.dataframe(

        df.head(max_rows),

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    st.subheader("Column Information")

    info = pd.DataFrame({

        "Column": df.columns,

        "Datatype": df.dtypes.astype(str),

        "Missing": df.isna().sum().values,

        "Missing %": (

            (df.isna().sum() / len(df)) * 100

        ).round(2),

        "Unique Values": df.nunique().values

    })

    st.dataframe(

        info,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    st.subheader("Missing Values")

    missing = df.isna().sum()

    missing = missing[missing > 0]

    if len(missing):

        st.dataframe(

            missing.reset_index().rename(

                columns={

                    "index": "Column",

                    0: "Missing"

                }

            ),

            use_container_width=True,

            hide_index=True

        )

    else:

        st.success("No Missing Values Found")

    st.divider()

    st.subheader("Duplicate Records")

    duplicates = df[df.duplicated()]

    if len(duplicates):

        st.dataframe(

            duplicates,

            use_container_width=True,

            hide_index=True

        )

    else:

        st.success("No Duplicate Rows Found")

    st.divider()

    st.download_button(

        "⬇ Download Filtered Dataset",

        df.to_csv(index=False).encode(),

        file_name="filtered_dataset.csv",

        mime="text/csv",

        use_container_width=True

    )