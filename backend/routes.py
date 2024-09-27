from app import app, db
from flask import request, jsonify
from models import User, Event
import re

# Get all users
# Query all users from db and return them as a list
@app.route("/api/users", methods = ["GET"]) # http://localhost/api/users url to see this table
def get_users():
    users = User.query.all()
    result = [user.to_json() for user in users]
    return jsonify(result), 200

# to view
@app.route("/api/register", methods = ["GET"])
def register_users():
    return "Hello, welcome to register"


def validate_email(email):
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    # Once we add database, add check that email is not already registered
    return re.match(email_regex, email) is not None


def validate_password(password):
    return len(password) > 0 and len(password) <= 128

# Register validation route
@app.route("/api/register", methods = ["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # validate email and password
    if not validate_email(email):
        return jsonify({"msg": "Invalid email"}), 400

    if not validate_password(password):
        return jsonify({"msg": "Invalid password"}), 400

    # if validations pass return success response
    return jsonify({"msg": "Registration successful"}), 200
