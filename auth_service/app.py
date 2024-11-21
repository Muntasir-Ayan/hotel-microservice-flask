from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated tokens and role management
tokens = {"admin_token": "Admin", "user_token": "User"}


@app.route("/validate-token", methods=["POST"])
def validate_token():
    token = request.headers.get("Authorization")
    role = tokens.get(token)
    if role:
        return jsonify({"role": role}), 200
    return jsonify({"error": "Invalid token"}), 403


if __name__ == "__main__":
    app.run(port=5003, debug=True)
