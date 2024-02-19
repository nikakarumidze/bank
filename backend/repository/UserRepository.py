import hashlib
from repository.DBConnection import DBConnection

class UserRepository:
    def __init__(self):
        self.db = DBConnection()
        # self.db.create_tables() # Only running once to create tables in db

    def register_user(self, username, password):
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            existing_user = self.db.cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if existing_user:
                return False, "User already exists"

            self.db.cursor.execute("INSERT INTO users (username, password_hash, balance) VALUES (?, ?, 5000)", (username, password_hash))
            self.db.conn.commit()
            return True, "User registered successfully"
        except Exception as e:
            return False, f"Error occurred while registering user: {e}"

    def authenticate_user(self, username, password):
        try:
            password_hash = hashlib.sha256(password.encode()).hexdigest()

            user = self.db.cursor.execute("SELECT * FROM users WHERE username = ? AND password_hash = ?", (username, password_hash)).fetchone()
            return user is not None
        except Exception as e:
            return (f"Error occurred while authenticating user: {e}")

    def get_user_balance(self, username):
        try:
            balance = self.db.cursor.execute("SELECT balance FROM users WHERE username = ?", (username,)).fetchone()
            return balance[0] if balance else None
        except Exception as e:
            return (f"Error occurred while getting user balance: {e}")

    def update_user_balance(self, username, new_balance):
        try:
            self.db.cursor.execute("UPDATE users SET balance = ? WHERE username = ?", (new_balance, username))
            self.db.conn.commit()
        except Exception as e:
            return (f"Error occurred while updating user balance: {e}")

    def get_user_transactions(self, username):
        try:
            user_id = self.db.cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,)).fetchone()
            if not user_id:
                return None  # User not found

            transactions = self.db.cursor.execute("SELECT * FROM transactions WHERE sender_id = ? OR receiver_id = ?", (user_id[0], user_id[0])).fetchall()
            return transactions
        except Exception as e:
            return (f"Error occurred while getting user transactions: {e}")
            return None

    def add_transaction(self, sender, receiver, amount):
        try:
            self.db.cursor.execute("INSERT INTO transactions (sender_id, receiver_id, amount, date) VALUES ((SELECT user_id FROM users WHERE username = ?), (SELECT user_id FROM users WHERE username = ?), ?, CURRENT_TIMESTAMP)", (sender, receiver, amount))
            self.db.conn.commit()
        except Exception as e:
            return (f"Error occurred while adding transaction: {e}")
