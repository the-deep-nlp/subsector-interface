import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


user = "postgres"
passwd = "postgres"
host = "localhost"
port = 5432
db = "postgres"

url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
engine = create_engine(url)

Session = sessionmaker(bind=engine)
session = Session()





# from tagger_page import TaggerPage


# class NewEntryPage:
#     def __init__(self):
#         pass

#     def create_page(self):
#         st.write("This is a new entry page")

# class SubSector:
#     def __init__(self):
#         self.tagger_page = TaggerPage()

#     def handle_tagger_page(self):
#         tagger_page.create_page()
    
#     def handle_newentry_page(self):
#         new_entry_page.create_page()
        

# subsector = SubSector()
# tagger_page = TaggerPage()
# new_entry_page = NewEntryPage()

# st.sidebar.write("Sub-Sector Menu")
# st.sidebar.button("Add Tagger", on_click=subsector.handle_tagger_page)
# st.sidebar.button("New Entry Tag", on_click=subsector.handle_newentry_page)
# st.sidebar.button("Edit Entry Tag")
# st.sidebar.button("View Entry Tags")