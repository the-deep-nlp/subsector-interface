import streamlit as st
import sqlalchemy as sa
import pandas as pd
import db_orm
import app
import json
from guidelines import guidelines

st.set_page_config(layout="wide")

class ViewEntryTag():
    def __init__(self):
        pass

    def _get_mapping(self, df):
        id_name_mapping = {}
        if len(df):
            id_name_lst = json.loads(df.to_json(orient="records"))
            for item in id_name_lst:
                id_name_mapping[item["id"]] = item["name"]
        return id_name_mapping


    def _get_list_of_users(self):
        df = pd.read_sql_table('Users', app.engine)
        return  ["All"] + df['name'].to_list(), self._get_mapping(df)
    
    @st.cache
    def generate_csv(self, df):
        return df.to_csv().encode("utf-8")

    def create_page(self):
        # Load Guidlines in the sidebar
        guidelines()

        list_of_users, id_name_mapping = self._get_list_of_users()
        selected_user = st.selectbox(
            "Select the Tagger",
            list_of_users
        )
        
        sa_table = sa.Table("Sectors", sa.MetaData(), autoload_with=app.engine)

        st.subheader("Data")
        if selected_user == "All":
            sa_query = sa.select([sa_table])
        else:
            selected_user_id = app.session.query(db_orm.Users).filter(db_orm.Users.name==selected_user).first().id
            sa_query = sa.select([sa_table]).where(
                sa_table.c.assigned_to==selected_user_id
            )

        df = pd.read_sql_query(sa_query, app.engine)
        if len(df):
            df["assigned_to"] = df["assigned_to"].map(id_name_mapping)
            st.dataframe(data=df, use_container_width=True)
            st.download_button(
                label="Download data as CSV",
                data=self.generate_csv(df),
                file_name="tagged_file.csv",
                mime="text/csv"
            )
        else:
            st.info("No related data found in the database.")
        


view_entry_tag = ViewEntryTag()
view_entry_tag.create_page()