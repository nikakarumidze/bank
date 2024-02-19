import sqlite3

class DBConnection:
    def __init__(self):
        self.conn = sqlite3.connect('Bank_database.db')
        self.cursor = self.conn.cursor()

    def create_tables(self):
        with open(r'C:\Users\nikak\bank\backend\init.sql', 'r') as file:
            sql_statements = file.read()
            self.cursor.executescript(sql_statements)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
