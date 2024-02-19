from flask import Flask, request, jsonify
from service.UserService import UserService

app = Flask(__name__)
user_service = UserService()

@app.route("/")
def index():
    return ['zd']

@app.route("/register", methods=['POST'])
def register_user():
    if request.method == 'POST':
        data = request.json
        result = user_service.register_user(data['username'], data['password'])
        if result:
            return result, 200
        else:
            return jsonify({"error": "Failed to register user"}), 400

if __name__=="__main__":
    app.run(debug=True)
