import streamlit as st

def guidelines():
    st.sidebar.subheader("Guidelines")
    st.sidebar.write(
        """1. Navigate to New Entry Tag page. If you have been assigned task, select your name and you will
        see tasks assigned in the progress bar. Go through the excerpt and select the relevant Sector, SubSector,
        SubSubSector"""
    )
    st.sidebar.write("2. Navigate to View Entry Tag page to have an overview of your work.")
    st.sidebar.write("3. Navigate to Edit Entry Tag page to edit an excerpt you have already tagged.")
    st.sidebar.write("4. Note that Upload CSV and New Tagger pages are for admins only.")