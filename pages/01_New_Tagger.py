import streamlit as st
import pandas as pd
import db_orm
import app
from guidelines import guidelines

class TaggerPage:
    def __init__(self):
        try:
            app.engine.connect()
            self.db_status = True
        except Exception:
            seld.db.status = False
            st.subheader("Database connection failed.")

    def create_page(self):
        st.header("Taggers")
        
        self.tagger_name = st.text_input("Tagger Name")

        self.submit_name = st.button("Submit")

        if self.submit_name:
            if self.db_write():
                st.success("Successfully added.")
            else:
                st.error("Error occurred while adding users.")
            
        
    def db_write(self):
        try:
            user = db_orm.Users(name=self.tagger_name)
            app.session.add(user)
            app.session.commit()
            return True
        except Exception as e:
            st.write(f"{str(e)}")
            return False
    
    def db_load_table(self):
        st.subheader("List of Taggers")
        df = pd.read_sql_table('Users', app.engine)
        df.set_index("id", inplace=True)
        df.rename(columns={'name': 'Tagger Name'}, inplace=True)
        st.table(df)

# Load Guidlines in the sidebar
guidelines()

if not st.session_state.get("ADMIN_PWD"):
    admin_password_user_add_pwd = st.text_input("Enter Admin Password", type="password", key='passwd2')
    if admin_password_user_add_pwd == st.secrets["ADMIN_PASSWORD"]:
        st.session_state["ADMIN_PWD"] = admin_password_user_add_pwd

if st.session_state.get("ADMIN_PWD", None):
    tagger_page = TaggerPage()
    if tagger_page.db_status:
        tagger_page.create_page()
        tagger_page.db_load_table()