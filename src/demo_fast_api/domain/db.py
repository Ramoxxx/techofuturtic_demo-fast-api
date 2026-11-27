import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


engine = create_engine(url=os.getenv('DB_URL'))
session_factory = sessionmaker(bind=engine)

def get_session():
    session = session_factory()
    yield session
    try:
        session.commit()
    finally:
        session.close()
