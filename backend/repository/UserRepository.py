from repository.DBConnection import DB_connection


class UserRepository:
    def __init__(self):
        self.db = DB_connection()
        self.db.create_tables()  # Only running once to create tables in db

    def user_exists(self, username):
        """Check if a user exists."""
        try:
            with self.db.conn:
                return self.db.cursor.execute(
                    "SELECT * FROM users WHERE username = ?", (username,)
                ).fetchone()
        except Exception:
            return "Error occurred", 400

    def is_email_used(self, email):
        """Check if an email is already in use."""
        try:
            return self.db.cursor.execute(
                "SELECT * FROM users WHERE email = ?", (email,)
            ).fetchone()
        except Exception:
            return "Error occurred", 400

    def register_user(self, User):
        """Register a new user."""
        try:
            self.db.cursor.execute(
                "INSERT INTO users (username, email, password_hash, balance) VALUES (?, ?, ?, ?)",
                (User.username, User.email, User.password_hash, User.balance),
            )
            self.db.conn.commit()
            return "User registered successfully", 200
        except Exception as e:
            return f"Error occurred while registering user: {e}", 400

    def authenticate_user(self, username, password):
        """Authenticate user."""
        user = self.db.cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, password),
        ).fetchone()
        return user is not None

    def get_user_balance(self, username):
        """Get user's balance."""
        try:
            balance = self.db.cursor.execute(
                "SELECT balance FROM users WHERE username = ?", (username,)
            ).fetchone()
            if not balance:
                raise ValueError()
            return balance[0]
        except Exception:
            return -1

    def update_user_balance(self, username, new_balance):
        """Update user's balance."""
        try:
            self.db.cursor.execute(
                "UPDATE users SET balance = ? WHERE username = ?",
                (new_balance, username),
            )
            self.db.conn.commit()
        except Exception as e:
            return f"Error occurred while updating user balance: {e}"

    def get_user_transactions(self, username):
        """Get user's transactions."""
        try:
            user_id = self.db.cursor.execute(
                "SELECT user_id FROM users WHERE username = ?", (username,)
            ).fetchone()
            if not user_id:
                return None  # User not found

            transactions = self.db.cursor.execute(
                "SELECT * FROM transactions WHERE sender_id = ? OR receiver_id = ?",
                (user_id[0], user_id[0]),
            ).fetchall()
            return transactions
        except Exception as e:
            return f"Error occurred while getting user transactions: {e}"

    def add_transaction(self, sender, receiver, amount):
        """Add a transaction."""
        try:
            self.db.cursor.execute(
                "INSERT INTO transactions (sender_id, receiver_id, amount, date) VALUES ((SELECT user_id FROM users WHERE username = ?), (SELECT user_id FROM users WHERE username = ?), ?, CURRENT_TIMESTAMP)",
                (sender, receiver, amount),
            )
            self.db.conn.commit()
        except Exception as e:
            return f"Error occurred while adding transaction: {e}"
