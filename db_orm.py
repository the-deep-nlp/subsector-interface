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
    modified_date = Column(Date, nullable=True)
    complete = Column(Boolean)
    assigned_to = Column(Integer, ForeignKey("Users.id"))

# add user as foreign key in sectors

if __name__ == "__main__":
    user = "postgres"
    passwd = "postgres"
    host = "localhost"
    port = 5432
    db = "postgres"

    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    engine = create_engine(url)
    Base.metadata.create_all(engine)