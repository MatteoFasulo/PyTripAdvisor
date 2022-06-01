import sqlite3
import os

import constants as const

# Database Structure and Config
def createDB(name = const.DB_NAME):
    if not os.path.isfile(name):
        conn = sqlite3.connect(name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE restaurants(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            restaurant_url TEXT NOT NULL,
            restaurant_name TEXT NOT NULL,
            restaurant_rating REAL,
            restaurant_total_reviews INTEGER,
            restaurant_price REAL
        );''')
        conn.commit()
        cursor.execute('''CREATE TABLE reviews(  
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            restaurant_url TEXT NOT NULL,
            reviewer_name TEXT NOT NULL,
            review_title TEXT NOT NULL,
            review_date TIMESTAMP NOT NULL,
            review_visit_date TIMESTAMP NOT NULL,
            review_rating INTEGER NOT NULL,
            review_helpful INTEGER,
            review_device TEXT,
            review_text TEXT NOT NULL,
            review_url TEXT NOT NULL
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
        return True

def exportSchema(name = const.DB_NAME):
    with open("sql_schema.txt", "w", encoding="utf-8") as schema:
        with sqlite3.connect(name) as con:
            cursor = con.cursor()
            cursor.execute('SELECT sql FROM sqlite_master')
            for r in cursor.fetchall():
                print(r[0], file=schema)
            cursor.close()
    return