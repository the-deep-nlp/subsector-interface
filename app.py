import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


user = "postgres"
passwd = "postgres"
host = "db"
port = 5432
db = "postgres"

url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
engine = create_engine(url)

Session = sessionmaker(bind=engine)
session = Session()
