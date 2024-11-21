from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger Config
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "User Service"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# In-memory user storage
users = {}


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    if email in users:
        return jsonify({"error": "User already exists"}), 400

    users[email] = {
        "name": data.get("name"),
        "email": email,
        "password": generate_password_hash(data.get("password")),
        "role": data.get("role", "User"),
    }
    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    user = users.get(email)

    if not user or not check_password_hash(user["password"], data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful", "role": user["role"]}), 200


@app.route("/profile", methods=["GET"])
def profile():
    email = request.headers.get("Email")
    user = users.get(email)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return (
        jsonify({"name": user["name"], "email": user["email"], "role": user["role"]}),
        200,
    )


if __name__ == "__main__":
    app.run(port=5002, debug=True)
