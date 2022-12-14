import streamlit as st
import sqlalchemy as sa
import pandas as pd
import db_orm
import app
import constants
import ast
from datetime import date
from guidelines import guidelines
from time import sleep

st.set_page_config(layout="wide")

class EditEntryTag():
    def __init__(self):
        pass

    def _get_list_of_users(self):
        df = pd.read_sql_table('Users', app.engine)
        return df['name'].to_list()


    def create_page(self):
        # Load Guidlines in the sidebar
        guidelines()

        selected_user = st.selectbox(
            "Select the Tagger",
            self._get_list_of_users()
        )

        selected_user_id = app.session.query(db_orm.Users).filter(db_orm.Users.name==selected_user).first().id

        selected_entry_id = st.number_input("Entry ID", min_value=1)

        sa_table = sa.Table("Sectors", sa.MetaData(), autoload_with=app.engine)
        sa_query = sa.select([sa_table]).where(
            sa_table.c.assigned_to==selected_user_id,
            sa_table.c.entry_id==selected_entry_id,
            sa_table.c.complete==True)
        df = pd.read_sql_query(sa_query, app.engine)

        # to fix the skipped rows
        #df = df.drop(labels=[0], axis=0).reset_index()

        try:
            sector_default = ast.literal_eval(df.iloc[0].sector)
        except Exception as e:
            sector_default = None
        
        try:
            subsector_default = ast.literal_eval(df.iloc[0].subsector)
        except Exception as e:
            subsector_default = None
        
        try:
            subsubsector_default = ast.literal_eval(df.iloc[0].subsubsector)
        except Exception as e:
            subsubsector_default = None

        if len(df):
            form = st.form('form', clear_on_submit=True)
            self.id = form.text_input("ID", value=df.iloc[0].id, disabled=True)
            self.excerpt = form.text_area("Excerpt", value=df.iloc[0].excerpt, disabled=True)
            
            self.sector = form.multiselect(
                "Sector",
                options=constants.sector_lst,
                default=sector_default
            )

            self.subsector = form.multiselect(
                "SubSector",
                options=constants.subsector_lst,
                default=subsector_default
            )
            
            self.subsubsector = form.multiselect(
                "SubSubSector",
                options=constants.subsubsector_lst,
                default=subsubsector_default
            )
            
            self.comment = form.text_area("Comment", value=df.iloc[0].comment)

            submit_btn = form.form_submit_button(label="Submit")
            if submit_btn:
                try:
                    app.session.query(db_orm.Sectors).filter(
                        db_orm.Sectors.entry_id==int(df.iloc[0].entry_id)
                    ).update(
                        {
                            "sector": str(self.sector),
                            "subsector": str(self.subsector),
                            "subsubsector": str(self.subsubsector),
                            "comment": str(self.comment),
                            "complete": True,
                            "last_tagged_date": date.today()
                        }
                    )
                    app.session.commit()
                    st.info("Database is updated.")
                except Exception as e:
                    st.error(f"Failed to update database. {e}")
                sleep(1)
                st.experimental_rerun()
        else:
            st.info("No record found.")


add_entry_tag = EditEntryTag()
add_entry_tag.create_page()