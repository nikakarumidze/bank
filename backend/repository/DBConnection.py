import sqlite3
import threading


class DB_connection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        # Implementing Singleton pattern
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    # Creating a new instance if none exists
                    cls._instance = super().__new__(cls)
                    # Establishing connection to SQLite database
                    cls._instance.conn = sqlite3.connect(
                        "Bank_database.db", check_same_thread=False
                    )
                    cls._instance.cursor = cls._instance.conn.cursor()
        return cls._instance

    def create_tables(self):
        # Create necessary tables in the database
        try:
            with open(r"C:\Users\nikak\bank\backend\init.sql", "r") as file:
                sql_statements = file.read()
                # Executing SQL statements to create tables
                self._instance.cursor.executescript(sql_statements)
            # Committing changes to the database
            self._instance.conn.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")

    def close_connection(self):
        # Close the database connection
        try:
            if self._instance:
                # Closing the connection if it exists
                self._instance.conn.close()
        except Exception as e:
            print(f"Error closing connection: {e}")
