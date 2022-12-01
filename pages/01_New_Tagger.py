import streamlit as st
import pandas as pd
import db_orm
import app
from guidelines import guidelines

st.set_page_config(layout="wide")

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
                st.success("Successfully added")
            else:
                st.error(f"{e}")
            
        
    def db_write(self):
        try:
            user = db_orm.Users(name=self.tagger_name)
            app.session.add(user)
            app.session.commit()
            return True
        except Exception as e:
            return e
    
    def db_load_table(self):
        st.subheader("List of Taggers")
        df = pd.read_sql_table('Users', app.engine)
        df.set_index("id", inplace=True)
        df.rename(columns={'name': 'Tagger Name'}, inplace=True)
        st.table(df)



tagger_page = TaggerPage()
tagger_page.create_page()
tagger_page.db_load_table()