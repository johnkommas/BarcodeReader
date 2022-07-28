#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

import pathlib
import sqlite3
from sqlite3 import Error
import pandas as pd
from private import pass_manager


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insertVaribleIntoSlackTable():
    try:
        parent_path = pathlib.Path(__file__).parent.resolve()
        database = f"{parent_path}/pythonsqlite.db"
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # GET DATA
        token_input = input("SLACK TOKEN: ")
        key, secrete_input = pass_manager.encrypt(input("SLACK SECRET: "))

        sqlite_insert_with_param = """INSERT INTO slack
                          (id, token, secrete, fernet) 
                          VALUES (?, ?, ?, ?);"""

        data_tuple = (1, token_input, secrete_input, key)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table (with Fernet encryption)")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def insertVaribleIntoSqlTable( data_tuple):
    try:
        parent_path = pathlib.Path(__file__).parent.resolve()
        database = f"{parent_path}/pythonsqlite.db"
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")


        sqlite_insert_with_param = """INSERT INTO EntersoftSql
                          (id, ServerIp, User_ID, PasswdKey, DataBaseName, TrustServerCertificate, fernet) 
                          VALUES (?, ?, ?, ?, ?, ?, ?);"""

        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table (with Fernet encryption)")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def insertVaribleIntoVpnTable( data_tuple):
    try:
        parent_path = pathlib.Path(__file__).parent.resolve()
        database = f"{parent_path}/pythonsqlite.db"
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")


        sqlite_insert_with_param = """INSERT INTO Vpn
                          (id, ConnectionName, PasswdKey, fernet) 
                          VALUES (?, ?, ?, ?);"""

        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into pythonsqlite.db table (with Fernet encryption)")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def read_credentials_for_entersoft_sql():
    parent_path = pathlib.Path(__file__).parent.resolve()
    database = f"{parent_path}/pythonsqlite.db"
    entersoft_query = "SELECT * FROM EntersoftSql WHERE id = 1"
    entersoft = pd.read_sql_query(entersoft_query, create_connection(database))
    return  entersoft


def read_credentials_for_vpn():
    parent_path = pathlib.Path(__file__).parent.resolve()
    database = f"{parent_path}/pythonsqlite.db"
    vpn_query = "SELECT * FROM Vpn WHERE id = 1"
    vpn = pd.read_sql_query(vpn_query, create_connection(database))
    return vpn


def read_token_for_slack():
    parent_path = pathlib.Path(__file__).parent.resolve()
    database = f"{parent_path}/pythonsqlite.db"
    slack_query = "SELECT * FROM slack WHERE id = 1"
    slack = pd.read_sql_query(slack_query, create_connection(database))
    return slack


def main():
    parent_path = pathlib.Path(__file__).parent.resolve()
    database = f"{parent_path}/pythonsqlite.db"

    sql_create_entersoft_table = """ CREATE TABLE IF NOT EXISTS EntersoftSql (
                                        id integer PRIMARY KEY,
                                        ServerIp nvarchar(255)                       not null,
                                        User_ID nvarchar(255)                       not null,
                                        PasswdKey nvarchar(255)                       not null,
                                        DataBaseName nvarchar(255)                       not null,
                                        TrustServerCertificate nvarchar(255)                       not null,
                                        fernet  nvarchar(255)                       not null   
                                    ); """

    sql_create_vpn_table = """ CREATE TABLE IF NOT EXISTS Vpn (
                                            id integer PRIMARY KEY,
                                            ConnectionName nvarchar(255)                       not null,
                                            PasswdKey nvarchar(255)                       not null,
                                            fernet  nvarchar(255)                       not null
                                        ); """
    sql_create_slack_table = """ CREATE TABLE IF NOT EXISTS slack (
                                            id integer PRIMARY KEY,
                                            token nvarchar(255)                       not null,
                                            secrete nvarchar(255)                       not null,
                                            fernet  nvarchar(255)                       not null
                                        ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_entersoft_table)
        create_table(conn, sql_create_vpn_table)
        create_table(conn, sql_create_slack_table)
    else:
        print("Error! cannot create the database connection.")

    # Query Database to see if they are empty
    entersoft_query = "SELECT id FROM EntersoftSql"
    slack_query = "SELECT id FROM slack"

    entersoft_id = pd.read_sql_query(entersoft_query, create_connection(database))
    slack_id = pd.read_sql_query(slack_query, create_connection(database))

    if slack_id.empty:
        insertVaribleIntoSlackTable()

    return entersoft_id.empty
