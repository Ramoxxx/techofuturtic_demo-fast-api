import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

load_dotenv()


def make_url(driver: str = "postgresql+psycopg") -> URL:
    return URL.create(
        driver,
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", "5432")),
        database=os.environ.get("DB_NAME", "pokemons"),
    )


engine = create_engine(
    make_url(),
    echo=os.environ.get("SQL_ECHO") == "1",
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)
