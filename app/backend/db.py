### - 2 и 3 занятие
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///taskmanager.db', echo = True)

SessionLocal = sessionmaker(bing=engine)

class Base (DeclarativeBase):
    pass
