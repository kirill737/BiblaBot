from database.dbapi import DatabaseConnector 
from database.models import *

from sqlalchemy import create_engine
import psycopg2
PORT = 5432


__all__ = ['models', 'dbapi', 'database']

connection_string = f"postgresql+psycopg2://:@localhost:{PORT}/biblabot"

if __name__ == "__main__":
    conn = psycopg2.connect(
        host = "localhost",
        port = PORT,
        database = "postgres",
        user = "",
        password = ""
    )
    conn.autocommit = True
    cursor = conn.cursor()
    sql = ''' CREATE database biblabot'''
    cursor.execute(sql)
    print("Biblabot has been created. Nobody can stop him.")
    conn.close()
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
