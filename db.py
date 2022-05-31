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
        conn.close()
        return True