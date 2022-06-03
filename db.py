#import sqlite3
import mysql.connector
import socket
import os

import constants as const

# Database Structure and Config
"""def createDB(name = const.DB_NAME):
    if not os.path.isfile(name):
        conn = sqlite3.connect(name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE restaurants(
            restaurant_url TEXT PRIMARY KEY NOT NULL,
            restaurant_name TEXT NOT NULL,
            restaurant_rating REAL,
            restaurant_total_reviews INTEGER,
            restaurant_price REAL,
            address TEXT
        );''')
        conn.commit()
        cursor.execute('''CREATE TABLE reviews( 
            review_url TEXT PRIMARY KEY NOT NULL, 
            restaurant_url TEXT NOT NULL,
            reviewer_name TEXT NOT NULL,
            review_title TEXT NOT NULL,
            review_date TIMESTAMP NOT NULL,
            review_visit_date TIMESTAMP NOT NULL,
            review_rating INTEGER NOT NULL,
            review_helpful INTEGER,
            review_device TEXT,
            review_text TEXT NOT NULL
        );''')
        conn.commit()
        cursor.execute('''CREATE TABLE reviewers(  
            reviewer_name TEXT PRIMARY KEY NOT NULL,
            profile_link TEXT NOT NULL,
            total_reviews INTEGER,
            reviewer_level INTEGER,
            user_since TIMESTAMP,
            home TEXT,
            total_cities INTEGER,
            total_helpful INTEGER
        );''')
        conn.commit()
        conn.close()
        return True"""

"""def exportSchema(name = const.DB_NAME):
    with open("sql_schema.txt", "w", encoding="utf-8") as schema:
        with sqlite3.connect(name) as con:
            cursor = con.cursor()
            cursor.execute('SELECT sql FROM sqlite_master')
            for r in cursor.fetchall():
                #print(r[0], file=schema)
            cursor.close()
    return"""

def query_unpack(query_result: list, key: str = None, unique: bool = False):
    final = []
    for i in range(len(query_result)):
        final.append(query_result[i].get(key))
    if unique is True:
        return list(set(final))
    else:
        return final

def db_connect():
    try:
        conn = mysql.connector.connect(host="127.0.0.1", user="root", password="NQIDWqGCF6n4P1vb")
        #print("[SQL] Connected")
        cursor = conn.cursor(buffered=True, dictionary=True)
        #print("[SQL] Cursor setup")
        cursor.execute("SHOW DATABASES")
        res = cursor.fetchall()
        dbs = query_unpack(res, "Database")
        if const.DB_NAME.strip() not in dbs:
            cursor.execute(f"CREATE DATABASE {const.DB_NAME}")
            cursor.execute(f"USE {const.DB_NAME}")
            cursor.execute(f"""CREATE TABLE {const.DB_NAME} (
                restaurant_url varchar(255) PRIMARY KEY NOT NULL,
                restaurant_name varchar(255) NOT NULL,
                restaurant_rating float,
                restaurant_total_reviews INTEGER,
                restaurant_price float,
                address varchar(255)
            )""")
            conn.commit()
            cursor.execute(f"""CREATE TABLE reviewers (  
                reviewer_name varchar(255) PRIMARY KEY NOT NULL,
                profile_link varchar(255) NOT NULL,
                total_reviews INTEGER,
                reviewer_level INTEGER,
                user_since date,
                home varchar(255),
                total_cities INTEGER,
                total_helpful INTEGER
            )""")
            conn.commit()
            conn.commit()
            cursor.execute(f"""CREATE TABLE reviews ( 
                review_url varchar(255) PRIMARY KEY NOT NULL, 
                restaurant_url varchar(255) NOT NULL,
                reviewer_name varchar(255) NOT NULL,
                review_title varchar(255) NOT NULL,
                review_date date NOT NULL,
                review_visit_date date NOT NULL,
                review_rating INTEGER NOT NULL,
                review_helpful INTEGER,
                review_device varchar(255),
                review_text varchar(255) NOT NULL
            )""")
            conn.commit()
            #print(f"[SQL] {const.DB_NAME} database created")

        #print(f"[SQL] {const.DB_NAME} database found")
        cursor.execute(f"USE {const.DB_NAME}")
        cursor.execute("SHOW TABLES")
        res = cursor.fetchall()
        query_unpack(res, f"Tables_in_{const.DB_NAME.strip()}")
        cursor = conn.cursor(buffered=True, dictionary=False)
        return conn, cursor

    except (mysql.connector.errors.InterfaceError, socket.gaierror) as err:
        print(f"[!] Got an exception, check your syntax --> {err}")
        return False

##########################################################

# SELECT restaurants.restaurant_url, COUNT(*) AS n_review
# FROM restaurants
# INNER JOIN reviews
# ON restaurants.restaurant_url = reviews.restaurant_url
# GROUP BY restaurants.restaurant_url
# ORDER BY n_review DESC;

##########################################################

##########################################################

# SELECT restaurants.restaurant_url, COUNT(*) AS n_review
# FROM restaurants
# INNER JOIN reviews
# ON restaurants.restaurant_url = reviews.restaurant_url
# GROUP BY restaurants.restaurant_url
# ORDER BY n_review DESC

##########################################################