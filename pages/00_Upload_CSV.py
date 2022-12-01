import streamlit as st
import pandas as pd
import app
import db_orm
from datetime import date

uploaded_file = st.file_uploader("Choose a csv file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    df["created_date"] = date.today()
    df["complete"] = False
    st.dataframe(df)

    records_updated =df.to_sql(
        "Sectors",
        con=app.engine,
        if_exists="append",
        index=True,
        index_label="id"
    )

    st.info(f"Records added to Database: {records_updated}")
