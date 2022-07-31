#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

import pathlib
import sqlite3
from sqlite3 import Error
import pandas as pd
from private import pass_manager
from app import plotter


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


def insertVariableIntoSlackTable():
    try:
        parent_path = pathlib.Path(__file__).parent.resolve()
        database = f"{parent_path}/pythonsqlite.db"
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        # GET DATA
        token_input = input("SLACK TOKEN: ")
        key, secret_input = pass_manager.encrypt(input("SLACK SECRET: "))

        sqlite_insert_with_param = """INSERT INTO Slack
                          (SlackToken, SlackSecret, KeyOnSave) 
                          VALUES (?, ?, ?);"""

        data_tuple = (token_input, secret_input, key)
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


def insertVariableIntoSqlTable(data_tuple):
    try:
        parent_path = pathlib.Path(__file__).parent.resolve()
        database = f"{parent_path}/pythonsqlite.db"
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO EntersoftSql
                          (ServerIp, User_ID, PasswdKey, DataBaseName, TrustServerCertificate, KeyOnSave) 
                          VALUES (?, ?, ?, ?, ?, ?);"""

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


def insertVariableIntoVpnTable(data_tuple):
    try:
        parent_path = pathlib.Path(__file__).parent.resolve()
        database = f"{parent_path}/pythonsqlite.db"
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO Vpn
                          (ConnectionName, PasswdKey, KeyOnSave) 
                          VALUES (?, ?, ?);"""

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


def insert_user_activity(data_tuple):
    try:
        parent_path = pathlib.Path(__file__).parent.resolve()
        database = f"{parent_path}/pythonsqlite.db"
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")


        sqlite_insert_with_param = """INSERT INTO Activity
                          (UserID, ChannelID) 
                          VALUES (?, ?);"""

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


def read_credentials_for_entersoft_sql():
    parent_path = pathlib.Path(__file__).parent.resolve()
    database = f"{parent_path}/pythonsqlite.db"
    entersoft_query = "SELECT * FROM EntersoftSql"
    entersoft = pd.read_sql_query(entersoft_query, create_connection(database))
    return entersoft


def read_credentials_for_vpn():
    parent_path = pathlib.Path(__file__).parent.resolve()
    database = f"{parent_path}/pythonsqlite.db"
    vpn_query = "SELECT * FROM Vpn"
    vpn = pd.read_sql_query(vpn_query, create_connection(database))
    return vpn


def read_token_for_slack():
    parent_path = pathlib.Path(__file__).parent.resolve()
    database = f"{parent_path}/pythonsqlite.db"
    slack_query = "SELECT * FROM Slack"
    slack = pd.read_sql_query(slack_query, create_connection(database))
    return slack


def read_activity():
    parent_path = pathlib.Path(__file__).parent.resolve()
    database = f"{parent_path}/pythonsqlite.db"
    slack_query = """
    SELECT UserID as "USER",
     ChannelID as "CHANNEL",
     count(*) AS "TIMES",
     strftime('%Y', TS) AS "YEAR" 
     FROM Activity
     GROUP BY UserID, ChannelID, strftime('%Y', TS)
     ORDER BY 2
    """
    activity = pd.read_sql_query(slack_query, create_connection(database))
    plotter.plot_activity(activity)
    return activity


def main():
    parent_path = pathlib.Path(__file__).parent.resolve()
    database = f"{parent_path}/pythonsqlite.db"

    sql_create_entersoft_table = """ CREATE TABLE IF NOT EXISTS EntersoftSql (
                                        GID integer PRIMARY KEY AUTOINCREMENT          NOT NULL,
                                        ServerIp nvarchar(255)                         NOT NULL,
                                        User_ID nvarchar(255)                          NOT NULL,
                                        PasswdKey nvarchar(255)                        NOT NULL,
                                        DataBaseName nvarchar(255)                     NOT NULL,
                                        TrustServerCertificate nvarchar(255)           NOT NULL,
                                        KeyOnSave  nvarchar(255)                       NOT NULL  
                                    ); """

    sql_create_vpn_table = """ CREATE TABLE IF NOT EXISTS Vpn (
                                            GID integer PRIMARY KEY AUTOINCREMENT      NOT NULL,
                                            ConnectionName nvarchar(255)               NOT NULL,
                                            PasswdKey nvarchar(255)                    NOT NULL,
                                            KeyOnSave  nvarchar(255)                   NOT NULL 
                                        ); """
    sql_create_slack_table = """ CREATE TABLE IF NOT EXISTS Slack (
                                            GID integer PRIMARY KEY AUTOINCREMENT      NOT NULL,
                                            SlackToken nvarchar(255)                   NOT NULL,
                                            SlackSecret nvarchar(255)                  NOT NULL,
                                            KeyOnSave  nvarchar(255)                   NOT NULL
                                        ); """

    sql_create_fingerprint_table = """ CREATE TABLE IF NOT EXISTS Activity (
                                            GID integer PRIMARY KEY AUTOINCREMENT      NOT NULL,
                                            UserID nvarchar(255)                       NOT NULL,
                                            ChannelID nvarchar(255)                    NOT NULL,
                                            TS  DATE DEFAULT (datetime('now','localtime'))          NOT NULL
                                        ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_entersoft_table)
        create_table(conn, sql_create_vpn_table)
        create_table(conn, sql_create_slack_table)
        create_table(conn, sql_create_fingerprint_table)
    else:
        print("Error! cannot create the database connection.")

    # Query Database to see if they are empty
    entersoft_query = "SELECT GID FROM EntersoftSql"
    slack_query = "SELECT GID FROM Slack"

    entersoft_id = pd.read_sql_query(entersoft_query, create_connection(database))
    slack_id = pd.read_sql_query(slack_query, create_connection(database))

    if slack_id.empty:
        insertVariableIntoSlackTable()

    return entersoft_id.empty
