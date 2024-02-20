from flask import Flask, request, jsonify, abort
from service.UserService import UserService

app = Flask(__name__)
user_service = UserService()


@app.route("/", methods=["POST"])
def get_user_info():
    if request.method == "POST":
        data = request.json
        result, status_code = user_service.get_user_data(
            data["username"], data["password"]
        )
        return jsonify(result) if status_code == 200 else abort(status_code, result)


@app.route("/register", methods=["POST"])
def register_user():
    if request.method == "POST":
        data = request.json
        result, status_code = user_service.register_user(
            data["username"], data["password"], data["email"]
        )
        return jsonify(result) if status_code == 200 else abort(status_code, result)


@app.route("/transactions", methods=["POST"])
def make_transaction():
    if request.method == "POST":
        data = request.json
        result, status_code = user_service.make_transaction(
            data["username"], data["password"], data["receiver"], data["amount"]
        )
        return jsonify(result) if status_code == 200 else abort(status_code, result)


if __name__ == "__main__":
    app.run(debug=True)
