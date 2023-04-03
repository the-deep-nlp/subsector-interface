import streamlit as st
import sqlalchemy as sa
import pandas as pd
import db_orm
import app
import json
from guidelines import guidelines
from sqlalchemy.sql import and_

st.set_page_config(layout="wide")

class ViewEntryTag():
    def __init__(self):
        self.rows_limit = 1_000
        try:
            app.engine.connect()
            self.db_status = True
        except Exception:
            self.db_status = False
            st.subheader("Database connection failed.")

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
    
    def get_query_for_all(self, sa_table, check_complete, check_reviewed, check_validated):
        if ((check_complete and check_reviewed and check_validated) or
            (check_complete and check_validated)):
            check_reviewed = True # if second condition is true, enforce reviewed to True
            sa_query = sa.select([sa_table]).where(
                and_(
                    sa_table.c.reviewed == check_reviewed,
                    sa_table.c.validated == check_validated
                )
            )
        elif check_complete and check_reviewed:
            sa_query = sa.select([sa_table]).where(
                sa_table.c.reviewed == check_reviewed # check_complete is not required to be checked
            )
        elif check_complete:
            sa_query = sa.select([sa_table]).where(
                sa_table.c.complete == check_complete
            )
        return sa_query

    def get_query_per_tagger(self, sa_table, selected_user_id, check_complete, check_reviewed, check_validated):
        if ((check_complete and check_reviewed and check_validated) or
            (check_complete and check_validated)):
            check_reviewed = True # if second condition is true, enforce reviewed to True
            
            sa_query = sa.select([sa_table]).where(
                and_(
                    sa_table.c.assigned_to==selected_user_id,
                    sa_table.c.reviewed==check_reviewed,
                    sa_table.c.validated==check_validated
                )
            )
        elif check_complete and check_reviewed:
            sa_query = sa.select([sa_table]).where(
                and_(
                    sa_table.c.assigned_to==selected_user_id,
                    sa_table.c.reviewed==check_reviewed # check_complete is not required to be checked
                )
            )
        elif check_complete:
            sa_query = sa.select([sa_table]).where(
                sa_table.c.assigned_to==selected_user_id,
                sa_table.c.complete==check_complete
            )
        return sa_query

    def create_page(self):
        # Load Guidlines in the sidebar
        guidelines()

        list_of_users, id_name_mapping = self._get_list_of_users()
        selected_user = st.selectbox(
            "Select the Tagger",
            list_of_users
        )

        def callb():
            if st.session_state.edit_validated:
                st.session_state.edit_reviewed = True

        st.subheader("Filters")
        select_options = st.radio("Choose the options", ("Show All", "Complete", "Incomplete"))
        if select_options == "Show All":
            check_show_all = True
        elif select_options == "Complete":
            check_show_all = False
            check_complete = True
            col1_reviewed, col2_validated = st.columns(2)
            with col1_reviewed:
                check_reviewed = st.checkbox("Reviewed", key="edit_reviewed")
            with col2_validated:
                check_validated = st.checkbox("Validated", key="edit_validated", on_change=callb)
        else:
            check_show_all = False
            check_complete = False
            check_incomplete = True

        sa_table = sa.Table("Sectors", sa.MetaData(), autoload_with=app.engine)

        st.subheader("Data")
        if selected_user == "All" and check_show_all:
            sa_query = sa.select([sa_table])
        elif selected_user == "All" and check_complete:
            sa_query = self.get_query_for_all(sa_table, check_complete, check_reviewed, check_validated)
        elif selected_user == "All" and check_incomplete:
            sa_query = sa.select([sa_table]).where(
                and_(
                    sa_table.c.complete==False,
                    sa_table.c.reviewed==False,
                    sa_table.c.validated==False
                )
            )
        elif selected_user != "All" and check_show_all:
            selected_user_id = app.session.query(db_orm.Users).filter(db_orm.Users.name==selected_user).first().id
            sa_query = sa.select([sa_table]).where(
                sa_table.c.assigned_to==selected_user_id
            )
        elif selected_user != "All" and check_complete:
            selected_user_id = app.session.query(db_orm.Users).filter(db_orm.Users.name==selected_user).first().id
            sa_query = self.get_query_per_tagger(
                sa_table,
                selected_user_id,
                check_complete,
                check_reviewed,
                check_validated
            )
        elif selected_user != "All" and check_incomplete:
            selected_user_id = app.session.query(db_orm.Users).filter(db_orm.Users.name==selected_user).first().id
            sa_query = sa.select([sa_table]).where(
                and_(
                    sa_table.c.assigned_to==selected_user_id,
                    sa_table.c.complete==False,
                    sa_table.c.reviewed==False,
                    sa_table.c.validated==False
                )
            )

        df = pd.read_sql_query(sa_query, app.engine)
        if len(df):
            df["assigned_to"] = df["assigned_to"].map(id_name_mapping)
            if len(df) > self.rows_limit:
                st.dataframe(data=df.sample(self.rows_limit), use_container_width=True)
                st.subheader("Note: Showing randomly selected 1000 rows only.")
            else:
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
if view_entry_tag.db_status:
    view_entry_tag.create_page()