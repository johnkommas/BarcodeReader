#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

import pandas as pd
import sqlite3
from my_app.SQL import database_path


def read(query):
    database = database_path.run()
    df = False
    con = False
    try:
        con = sqlite3.connect(database)
        df = pd.read_sql_query(query, con)
    except Exception as e:
        print(f"Connection Corrupted: {e}")
    finally:
        con.close()
        return df


def write(database_name, sql_columns, data_tuple):
    sqliteConnection = False
    try:
        database = database_path.run()
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"""
                INSERT INTO {database_name}
                {sql_columns}
                VALUES {data_tuple};
                 """
        cursor.execute(query)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table ")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
