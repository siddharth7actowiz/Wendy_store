from config import *
import mysql.connector

def make_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn
def create_Table(cursor,TAB):
    ddl=f'''CREATE TABLE IF NOT EXISTS {TAB} (
            id  INT AUTO_INCREMENT PRIMARY KEY,
           Name VARCHAR(100),
           Map VARCHAR(500),
           StreetAddress VARCHAR(200),
           City VARCHAR(20),
           State VARCHAR(20),
           Country VARCHAR(20),
           Pincode VARCHAR(50),
           Phone_Number VARCHAR(100),
           Restaurant_Hours TEXT,
           DriveThru_Hours TEXT,
           DeliveryOption TEXT,
           CurrentlyOperating TEXT,
          Menu_Items TEXT
        );'''
    cursor.execute(ddl)

def insert_into_db(data, cursor, con):
    if not data:                          
        print("No data to insert.")
        return
    # handle both single dict and list of dicts
    if isinstance(data, dict):
        data = [data]
    try:
        cols   = ",".join(data[0].keys())
        vals   = ",".join(["%s"] * len(data[0].keys()))
        insert_query = f"INSERT INTO {TABLE_NAME} ({cols}) VALUES ({vals});"
        rows   = [tuple(d.values()) for d in data]
        cursor.executemany(insert_query, rows)
        con.commit()
        print(f"{cursor.rowcount} rows inserted.")
    except Exception as e:
        con.rollback()
        print("Error", insert_into_db.__name__, e)