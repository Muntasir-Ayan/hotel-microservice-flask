from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
import json
import os

app = Flask(__name__)

# swagger
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

# File path to store the data
data_file_path = "access_data.json"


@app.route("/")
def home():
    return jsonify({"Message": "Hello message is running successfully w3"})


@app.route("/access", methods=["POST"])
def access():
    # Get JSON data from the request
    data = request.get_json()

    name = data.get("name", "dipto")
    server = data.get("server", "server1")

    message = f"User {name} received access to server {server}"

    # Store the data into a file locally
    store_data_locally(data)

    return jsonify({"Message": message})


def store_data_locally(data):
    # Check if file exists, if not create it and store an empty list
    if not os.path.exists(data_file_path):
        with open(data_file_path, "w") as f:
            json.dump([], f)

    # Read current data from the file
    with open(data_file_path, "r") as f:
        current_data = json.load(f)

    # Append the new data
    current_data.append(data)

    # Write updated data back to the file
    with open(data_file_path, "w") as f:
        json.dump(current_data, f, indent=4)


# Swagger UI blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Access API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
