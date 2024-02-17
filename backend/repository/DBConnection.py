import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        with open('../init.sql', 'r') as file:
            sql_statements = file.read()
            self.cursor.executescript(sql_statements)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
