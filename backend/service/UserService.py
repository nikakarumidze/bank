import re
import hashlib
from repository.UserRepository import UserRepository


class UserService:
    def __init__(
        self,
    ):
        self.repo = UserRepository()

    def __user_exists(self, username):
        return self.repo.user_exists(username)

    def __is_valid_email(self, email):
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(regex, email) is not None

    def __is_email_used(self, email):
        return self.repo.is_email_used(email) is not None

    def register_user(self, username, password, email):
        if len(username) < 4:
            return "Not sufficient characters for user", 400
        if 8 > len(password) < 26:
            return "The length of password should be between 8 and 26 characters", 400
        if not bool(re.search(r"\d", password)):
            return {"error": "Password must contain at least one digit"}, 400
        if self.__user_exists(username) is not None:
            return {"error": "User Exists"}, 400
        if not self.__is_valid_email(email):
            return {"error": "Please type correct email"}, 400
        if self.__is_email_used(email):
            return {"error": "The email already exists"}, 400

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.repo.register_user(username, email, password_hash)

    def __authenticate_user(self, username, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.repo.authenticate_user(username, password_hash)

    def __get_user_balance(self, username):
        return self.repo.get_user_balance(username)

    def __get_user_transactions(self, username):
        return self.repo.get_user_transactions(username)

    def get_user_data(self, username, password):
        access = self.__authenticate_user(username, password)
        if access:
            balance = self.__get_user_balance(username)
            transactions = self.__get_user_transactions(username)
            return [balance, transactions], 200
        return {"error": "Incorrect Username or Password"}, 400

    def make_transaction(self, username, password, receiver, amount):
        access = self.__authenticate_user(username, password)
        if access:
            return self.__add_transaction(username, receiver, amount)
        return {"error": "Incorrect Password"}, 400

    def __add_transaction(self, sender, receiver, amount):
        sender_balance = self.repo.get_user_balance(sender)
        receiver_balance = self.repo.get_user_balance(receiver)

        if sender_balance is None or receiver_balance is None:
            return {"error": "Error occured"}, 400
        if sender_balance <= amount:
            return {"error": "Not sufficient balance"}, 400

        self.repo.add_transaction(sender, receiver, amount)
        # Update user balances
        self.repo.update_user_balance(sender, sender_balance - amount)
        self.repo.update_user_balance(receiver, receiver_balance + amount)
        return "Success", 200
