#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

# Make the Connection
import pyodbc
import sys
import os
from subprocess import call, check_output
import time
import socket
from private.credentials import ip, c


def connect():
    sql_counter = 0
    my_ip = get_ip_address()
    try:
        credits = c['sql_server_credentials']
        cnxn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};"
                              f"Server={credits.get('Server')};"  # <-- HERE GOES SQL SERVER IP
                              f"UID={credits.get('UID')};"  # <-- HERE GOES SQL USER
                              f"PWD={credits.get('PWD')};"  # <-- HERE GOES SQL CREDENTIALS
                              f"Database={credits.get('Database')};"  # <-- HERE GOES DATABASE 
                              f"TrustServerCertificate={credits.get('TrustServerCertificate')}")
    except pyodbc.OperationalError:
        print(f"\n🔴: (!SQL!) Working Remotely: My IP ADDRESS is {my_ip}")
        return open_vpn(sql_counter)
    return cnxn


def open_vpn(sql_counter):
    EM_mode = os.system(f"ping -c 1  {ip.get('EM')} >/dev/null")
    if EM_mode == 0:
        credits = c['vpn_credentials']
        print("\n🟢: (SQL) Elounda Market is UP, Trying to get VPN UP...")
        call(["scutil", "--nc", "start", credits.get('name'), '--secret', credits.get('secret')])
        time.sleep(5)
        Server_mode = os.system(f"ping -c 1  {ip.get('EM ROUTER')} >/dev/null")
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


