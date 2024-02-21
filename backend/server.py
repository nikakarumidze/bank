from flask import Flask, request, jsonify, abort, json
from werkzeug.exceptions import HTTPException
from service.UserService import UserService
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize UserService
user_service = UserService()


# Route for user login
@app.route("/login", methods=["POST"])
def get_user_info():
    if request.method == "POST":
        data = request.json
        # Call UserService method to get user data
        result, status_code = user_service.get_user_data(
            data.get("username"), data.get("password")
        )
        return jsonify(result) if status_code == 200 else abort(status_code, result)


# Route for user signup
@app.route("/signup", methods=["POST"])
def register_user():
    if request.method == "POST":
        data = request.json
        # Call UserService method to register user
        result, status_code = user_service.register_user(
            data.get("username"), data.get("password"), data.get("email")
        )
        return jsonify(result) if status_code == 200 else abort(status_code, result)


# Route for making transactions
@app.route("/transactions", methods=["POST"])
def make_transaction():
    if request.method == "POST":
        data = request.json
        # Call UserService method to make transaction
        result, status_code = user_service.make_transaction(
            data.get("username"),
            data.get("password"),
            data.get("receiver"),
            data.get("amount"),
        )
        return jsonify(result) if status_code == 200 else abort(status_code, result)


# Error handler for HTTP exceptions
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # Create JSON response for the error
    response = e.get_response()
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
