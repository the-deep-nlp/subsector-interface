import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Float, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Sectors(Base):
    __tablename__ = "Sectors"

    id = Column(Integer, primary_key=True)
    entry_id = Column(Integer)
    excerpt = Column(String)
    sector = Column(String)
    subsector = Column(String, nullable=True)
    subsubsector = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    created_date = Column(Date, nullable=True)
    last_tagged_date = Column(Date, nullable=True)
    complete = Column(Boolean)
    assigned_to = Column(Integer, ForeignKey("Users.id"))

if __name__ == "__main__":
    user = os.environ.get("POSTGRES_USER")
    passwd = os.environ.get("POSTGRES_PASSWORD")
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", 5432)
    db = os.environ.get("POSTGRES_DB")

    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    engine = create_engine(url)
    Base.metadata.create_all(engine)