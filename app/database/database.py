from sqlalchemy import create_engine, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import url


Base = declarative_base()
engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
