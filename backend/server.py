from flask import Flask, request, jsonify, abort, json
from werkzeug.exceptions import HTTPException
from service.UserService import UserService
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
user_service = UserService()


@app.route("/login", methods=["POST"])
def get_user_info():
    if request.method == "POST":
        data = request.json
        result, status_code = user_service.get_user_data(
            data["username"], data["password"]
        )
        return (
            jsonify(result)
            if status_code == 200
            else abort(status_code, jsonify(result))
        )


@app.route("/signup", methods=["POST"])
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


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


if __name__ == "__main__":
    app.run(debug=True)
