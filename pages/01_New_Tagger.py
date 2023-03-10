import streamlit as st
import pandas as pd
import db_orm
import app
from guidelines import guidelines

class TaggerPage:
    def __init__(self):
        pass

    def create_page(self):
        # Load Guidlines in the sidebar
        guidelines()

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


admin_password_user_add = st.text_input("Enter Admin Password", type="password", key='passwd2')
if admin_password_user_add == st.secrets["ADMIN_PASSWORD"]:
    tagger_page = TaggerPage()
    tagger_page.create_page()
    tagger_page.db_load_table()