from repository.UserRepository import UserRepository

class UserService:
    def __init__(self, db_name):
        self.repo = UserRepository(db_name)

    def register_user(self, username, password):
        self.repo.register_user(username, password)

    def authenticate_user(self, username, password):
        return self.repo.authenticate_user(username, password)

    def get_user_balance(self, username):
        return self.repo.get_user_balance(username)

    def get_user_transactions(self, username):
        return self.repo.get_user_transactions(username)

    def add_transaction(self, sender, receiver, amount):
        sender_balance = self.repo.get_user_balance(sender)
        receiver_balance = self.repo.get_user_balance(receiver)

        if sender_balance is None or receiver_balance is None:
            return 'Error occured'
        elif sender_balance <= amount:
            return 'Not sufficient balance'
        else:
            self.repo.add_transaction(sender, receiver, amount)
            # Update user balances
            self.repo.update_user_balance(sender, sender_balance-amount)
            self.repo.update_user_balance(receiver, receiver_balance+amount)
            return 'Success'