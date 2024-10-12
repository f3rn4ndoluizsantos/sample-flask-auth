from flask import Blueprint, jsonify

# Create a Blueprint
router_users = Blueprint("router", __name__)


@router_users.route("/hello", methods=["GET"])
def hello():
    return jsonify(message="Hello, World!")


@router_users.route("/goodbye", methods=["GET"])
def goodbye():
    return jsonify(message="Goodbye, World!")
