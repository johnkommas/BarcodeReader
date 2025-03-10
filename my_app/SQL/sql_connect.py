#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved


# Make the Connection
import pyodbc
from subprocess import call
import time
import socket
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def connect():
    load_dotenv()
    sql_counter = 0
    my_ip = get_ip_address()
    try:
        cnxn = f"""DRIVER={{ODBC Driver 17 for SQL Server}};
                                      Server={os.getenv('SQL_SERVER')};
                                      UID={os.getenv('UID')};
                                      PWD={os.getenv('SQL_PWD')};
                                      Database={os.getenv('DATABASE')};
                                      TrustServerCertificate={os.getenv('TSC')}"""
        connection_string = cnxn
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        engine = create_engine(connection_url)
    except pyodbc.OperationalError:
        print(f"\n🔴: (!SQL!) Working Remotely: My IP ADDRESS is {my_ip}")
        return open_vpn(sql_counter)
    return engine


def open_vpn(sql_counter):
    EM_mode = os.system(f"ping -c 1  {os.getenv('VPN')} >/dev/null")
    if EM_mode == 0:
        print("\n🟢: (SQL) is UP, Trying to get VPN UP...")
        call(["scutil", "--nc", "start", os.getenv('VPN_NAME'), '--secret', os.getenv('VPN_PWD')])
        time.sleep(5)
        Server_mode = os.system(f"ping -c 1  {os.getenv('ROUTER')} >/dev/null")
        if Server_mode == 0:
            print("🟢: (SQL) VPN IS UP")
            return connect()
        else:
            sql_counter += 1
            print(f"\r🔴: (SQL) VPN IS STILL DOWN || Tries: {sql_counter}", end='')
            return open_vpn(sql_counter)

    else:
        sql_counter += 1
        print(f"\r🔴: (SQL) Internet on Site Is Down || Tries: {sql_counter}", end='')
        return open_vpn(sql_counter)


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
