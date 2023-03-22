import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from guidelines import guidelines

user = os.environ.get("POSTGRES_USER")
passwd = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST", "db")
port = os.environ.get("POSTGRES_PORT", 5432)
db = os.environ.get("POSTGRES_DB")

st.set_page_config(layout="wide")

guidelines()

try:
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    engine = create_engine(url, connect_args={'connect_timeout': 5})

    Session = sessionmaker(bind=engine)
    session = Session()
    engine.connect()
    # Load Guidelines
    st.subheader("Database connection established. Go through the guidelines and Navigate to other pages.")
except Exception as e:
    st.subheader("Database connection failed.")
