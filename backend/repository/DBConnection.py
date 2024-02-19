import sqlite3

class DBConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect('Bank_database.db')
            cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance

    def create_tables(self):
        with open(r'C:\Users\nikak\bank\backend\init.sql', 'r') as file:
            sql_statements = file.read()
            self.cursor.executescript(sql_statements)
        self.conn.commit()

    def close_connection(self):
        self.conn.close()