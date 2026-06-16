import sqlite3

DB_FILE = "data/airpct.db"

def get_connection():
    return sqlite3.connect(DB_FILE)

