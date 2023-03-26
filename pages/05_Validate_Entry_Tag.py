import streamlit as st
import sqlalchemy as sa
import pandas as pd
import db_orm
import app
import json
from guidelines import guidelines
from time import sleep

class ValidateEntryTag():
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

    def create_page(self):
        list_of_users, id_name_mapping = self._get_list_of_users()
        selected_user = st.selectbox(
            "Select the Tagger",
            list_of_users
        )
        
        sa_table = sa.Table("Sectors", sa.MetaData(), autoload_with=app.engine)

        st.subheader("Data")
        if selected_user == "All":
            sa_query = sa.select([sa_table]).where(
                (sa_table.c.complete==True) &
                (sa_table.c.validated==False)
            )
        else:
            selected_user_id = app.session.query(db_orm.Users).filter(db_orm.Users.name==selected_user).first().id
            sa_query = sa.select([sa_table]).where(
                (sa_table.c.assigned_to==selected_user_id) &
                (sa_table.c.complete==True) &
                (sa_table.c.validated==False)
            )

        df = pd.read_sql_query(sa_query, app.engine)

        if len(df):
            df["assigned_to"] = df["assigned_to"].map(id_name_mapping)

            st.subheader(f"Entry ID: {df.iloc[0].entry_id}")
            st.write(f"Excerpt: {df.iloc[0].excerpt}")
            st.write(f"Sector: {df.iloc[0].sector}")
            st.write(f"Subsector: {df.iloc[0].subsector}")
            st.write(f"Subsubsector: {df.iloc[0].subsubsector}")
            st.write(f"Subsubsubsector: {df.iloc[0].subsubsubsector}")
            st.write(f"Subsubsubsubsector: {df.iloc[0].subsubsubsubsector}")
            st.write(f"Tagged By: {df.iloc[0].assigned_to}")
            validated = st.checkbox("Validate", value=False)
            reviewed = st.checkbox("Reviewed", value=False)
            supervisor_comment = st.text_area("Supervisor Comment", value=df.iloc[0].supervisor_comment)
            if validated and reviewed:
                complete = True
            elif not validated and reviewed:
                complete = False
            else:
                complete = True # only True items are queried, so, status remains True
            if validated:
                reviewed=True

            submit = st.button("Submit")
            if submit:
                try:
                    app.session.query(db_orm.Sectors).filter(
                        db_orm.Sectors.entry_id==int(df.iloc[0].entry_id)
                    ).update(
                        {
                            "validated": validated,
                            "reviewed": reviewed,
                            "supervisor_comment": str(supervisor_comment),
                            "complete": complete
                        }
                    )
                    app.session.commit()
                    st.info("Database is updated.")
                except Exception as e:
                    st.error(f"Failed to update database. {e}")
                sleep(1)
                st.experimental_rerun()
        else:
            st.info("No related data found in the database.")

# Load Guidlines in the sidebar
guidelines()
validation_password = st.text_input("Enter the Password", type="password", key='passwd3')
if validation_password == st.secrets["VALIDATION_PASSWORD"]:
    validate_entry_tag = ValidateEntryTag()
    if validate_entry_tag.db_status:
        validate_entry_tag.create_page()
