import streamlit as st
import pandas as pd
import app
import db_orm
from datetime import date
from guidelines import guidelines


guidelines() # Load Guidlines in the sidebar

admin_password_upload_page = st.text_input("Enter Admin Password", type="password", key='passwd1')

if admin_password_upload_page == st.secrets["ADMIN_PASSWORD"]:
    uploaded_file = st.file_uploader("Choose a csv file")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        df["created_date"] = date.today()
        df["complete"] = False
        st.dataframe(df)
        df.reset_index(drop=True, inplace=True)
        records_updated = df.to_sql(
            "Sectors",
            con=app.engine,
            if_exists="append",
            index=False,
            index_label="id"
        )

        st.info(f"Records added to Database: {records_updated}")
