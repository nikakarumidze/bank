import re
import hashlib
from repository.UserRepository import UserRepository
from model.User import User


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def __user_exists(self, username):
        """Check if the user exists."""
        return self.repo.user_exists(username)

    def __is_valid_email(self, email):
        """Validate email using regex."""
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(regex, email) is not None

    def __is_email_used(self, email):
        """Check if email is already in use."""
        return self.repo.is_email_used(email) is not None

    def register_user(self, username, password, email):
        """Register a new user."""
        if len(username) < 4:
            return "Not sufficient characters for username", 400
        if not (8 <= len(password) <= 26):
            return "The password length should be between 8 and 26 characters", 400
        if not bool(re.search(r"\d", password)):
            return "Password must contain at least one digit", 400
        if self.__user_exists(username):
            return "User already exists", 400
        if not self.__is_valid_email(email):
            return "Please enter a valid email address", 400
        if self.__is_email_used(email):
            return "The email address is already in use", 400

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.repo.register_user(User(username, password_hash, email, 5000, []))

    def __authenticate_user(self, username, password):
        """Authenticate user."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.repo.authenticate_user(username, password_hash)

    def __get_user_balance(self, username):
        """Get user's balance."""
        return self.repo.get_user_balance(username)

    def __get_user_transactions(self, username):
        """Get user's transactions."""
        return self.repo.get_user_transactions(username)

    def get_user_data(self, username, password):
        """Get user's data (balance and transactions)."""
        access_granted = self.__authenticate_user(username, password)
        if not access_granted:
            return "Incorrect Username or Password", 400
        balance = self.__get_user_balance(username)
        transactions = self.__get_user_transactions(username)
        return {"balance": balance, "transactions": transactions}, 200

    def make_transaction(self, username, password, receiver, amount):
        """Make a transaction."""
        access = self.__authenticate_user(username, password)
        if access:
            return self.__add_transaction(username, receiver, amount)
        return "Incorrect Password", 400

    def __add_transaction(self, sender, receiver, amount):
        """Add a transaction."""
        amount = int(amount)
        sender_balance = self.repo.get_user_balance(sender)
        receiver_balance = self.repo.get_user_balance(receiver)

        if sender_balance is None or receiver_balance is None:
            return "Error occurred. Please check receiver username", 400
        if sender_balance < amount:
            return "Not enough balance", 400

        self.repo.add_transaction(sender, receiver, amount)
        # Update user balances
        self.repo.update_user_balance(sender, sender_balance - amount)
        self.repo.update_user_balance(receiver, receiver_balance + amount)
        return "Success", 200
