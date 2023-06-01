#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

# Make the Connection
import os
from subprocess import call
import time
import socket
from my_app.SQL import sql3_conn, pass_manager
# from sqlalchemy.engine import URL
# from sqlalchemy import create_engine
import pyodbc



def connect():
    sql_counter = 0
    my_ip = get_ip_address()
    df = sql3_conn.read_credentials_for_entersoft_sql()
    try:
        cnxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                              f"Server={df['ServerIp'].values[0]};"  
                              f"UID={df['User_ID'].values[0]};"  
                              f"PWD={pass_manager.decrypt(df['KeyOnSave'].values[0], df['PasswdKey'].values[0])};"  
                              f"Database={df['DataBaseName'].values[0]};"  
                              f"TrustServerCertificate={df['TrustServerCertificate'].values[0]}")
        # connection_string = cnxn
        # connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        # engine = create_engine(connection_url, pool_pre_ping=True)
    except :
        print(f"\n🔴: (!SQL!) Working Remotely: My IP ADDRESS is {my_ip}")
        return open_vpn(sql_counter)
    return cnxn


def open_vpn(sql_counter):
    df = sql3_conn.read_ip()
    EM_mode = os.system(f"ping -c 1  {df['BotID'][['BOtName'] == 'EM'].values[0]} >/dev/null")
    if EM_mode == 0:
        df = sql3_conn.read_credentials_for_vpn()
        print("\n🟢: (SQL) Elounda Market is UP, Trying to get VPN UP...")
        call(["scutil", "--nc", "start", df['ConnectionName'].values[0], '--secret', pass_manager.decrypt(df['KeyOnSave'].values[0], df['PasswdKey'].values[0])])
        time.sleep(5)
        Server_mode = os.system(f"ping -c 1  {df['BotID'][['BOtName'] == 'EM ROUTER'].values[0]} >/dev/null")
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
