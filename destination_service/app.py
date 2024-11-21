from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger Config
SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Destination Service"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# In-memory data storage
destinations = {
    1: {"name": "Paris", "description": "City of Light", "location": "France"},
    2: {"name": "Tokyo", "description": "Land of Rising Sun", "location": "Japan"},
}


@app.route("/")
def first_page():
    return "hello world"


@app.route("/destinations", methods=["GET"])
def get_destinations():
    return jsonify(list(destinations.values())), 200


@app.route("/destinations/<int:destination_id>", methods=["DELETE"])
def delete_destination(destination_id):
    # Simulate Admin role-based access (needs proper auth service integration)
    if request.headers.get("Role") != "Admin":
        return jsonify({"error": "Unauthorized"}), 403
    if destination_id in destinations:
        del destinations[destination_id]
        return jsonify({"message": "Destination deleted successfully"}), 200
    return jsonify({"error": "Destination not found"}), 404


if __name__ == "__main__":
    app.run(port=5001, debug=True)
