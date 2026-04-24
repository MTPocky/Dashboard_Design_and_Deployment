from sqlalchemy import create_engine, text
from app.setting import DATABASE_URL, TABLE_NAME


engine = create_engine(DATABASE_URL)


def fetch_one(query: str):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        row = result.fetchone()
        if row is None:
            return None
        return dict(row._mapping)


def fetch_all(query: str):
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return [dict(row._mapping) for row in result]


def table_name():
    return TABLE_NAME