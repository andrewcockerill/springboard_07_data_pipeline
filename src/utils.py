# Packages
import mysql.connector
import os
from dotenv import load_dotenv
import re
import calendar
import datetime

def get_db_connection():
    # Retrieve a MySQL connection object

    # Vars
    conn = None
    load_dotenv()
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    HOST = os.getenv("HOST")
    PORT = os.getenv("PORT")

    # Try connection
    try:
        conn = mysql.connector.connect(
            user = DB_USER,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT
        )
    except Exception as e:
        print("Error while connecting to database for job tracker", e)

    return conn

def load_third_party(conn, path):
    # Load datasets into MySQL database

    # Cursor and vars
    db_name = "ticketing"
    tbl_name = "sales"
    cursor = conn.cursor()

    try:

        # DB/Table Setup
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        cursor.execute(f"DROP TABLE IF EXISTS {db_name}.{tbl_name};")
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {db_name}.{tbl_name}
            (
            ticket_id INT,
            trans_date INT,
            event_id INT,
            event_name VARCHAR(50),
            event_date DATE,
            event_type VARCHAR(10),
            event_city VARCHAR(20),
            customer_id INT,
            price DECIMAL(10,2),
            num_tickets INT
            );""")
        
        conn.commit()

        # Insertions
        def insert_statement(rec):
            return f"""
            INSERT INTO {db_name}.{tbl_name}
            (ticket_id, trans_date, event_id, event_name, event_date, event_type, event_city, customer_id, price, num_tickets)
            VALUES {rec};"""
        
        with open(path, 'r') as f:
            reader = f.readlines()
            insertions = []
            for line in reader:
                parsed_line = line.strip().split(',')
                for i in [3,4,5,6]:
                    parsed_line[i] = f'"{parsed_line[i]}"'

                parsed_line = f"({",".join(parsed_line)})"
                insertions.append(parsed_line)
            insertions = ','.join(insertions)
            
            insert_statement = f"""
            INSERT INTO {db_name}.{tbl_name}
            (ticket_id, trans_date, event_id, event_name, event_date, event_type, event_city, customer_id, price, num_tickets)
            VALUES {insertions};"""

            cursor.execute(insert_statement)
            conn.commit()


    except Exception as e:
        print("Unexpected error when attempting table setup and insertion", e)
    finally:
        cursor.close()

def query_popular_tickets(conn):
    # Get the most popular ticketed events all time
    query = """
    WITH total_sales AS
    (SELECT event_name, SUM(num_tickets) AS sales
    FROM ticketing.sales
    GROUP BY event_name)

    SELECT event_name
    FROM total_sales
    ORDER BY sales DESC
    LIMIT 3;
    """
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        print('Here are the most popular ticketed events all time:')
        for rec in records:
            print(f"- {rec[0]}")
    except Exception as e:
        print("Unexpected error when querying top tickets", e)
    finally:
        cursor.close()
