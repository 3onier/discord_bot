import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import MySQLdb

engine = create_engine(
    f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@" +
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session: Session = Session()
