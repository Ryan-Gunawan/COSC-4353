from app import app, db
from flask import Flask, request, jsonify, session, redirect, url_for
import json
from models import User, Event
import re
import os

app.secret_key = 'secretkey'
USER_FILE = 'dummy/users.json'

### Login and Registration Routes and Functions ###

# Get all users
# Query all users from db and return them as a list
@app.route("/api/users", methods = ["GET"]) # http://localhost/api/users url to see this table
def get_users():
    users = User.query.all()
    result = [user.to_json() for user in users]
    return jsonify(result), 200

@app.route("/api/eventlist", methods = ["GET"])
def get_events():
    events = Event.query.all()
    result = [event.to_json() for event in events]
    #return jsonify(result), 200
    event_1 = 'Event 1-----zfeahrhu'
    return jsonify(event_1, result), 200

@app.route("/api/newevent", methods = ["POST"])
def post_event():
    data = request.get_json()
    name = data.get("name")
    location = data.get("location")

@app.route("/api/register", methods = ["GET"])
def register_users():
    return "Hello, welcome to register"

# Loads user data from json file. Simulates loading from a database for testing
def load_users():
    if not os.path.exists(USER_FILE):
        return {"users": []} # if no file, return empty string
    with open(USER_FILE, 'r') as f:
        return json.load(f) # returns user json object as dictionary

# Saves updated users.json
def save_users(data):
    with open(USER_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Function to get user by email
def get_user_by_email(email):
    data = load_users()
    for user in data['users']:
        if user['email'].lower() == email.lower(): # ignore case sensitivity
            return user
    return None

# Function to add new user
def add_user(email, password):
    data = load_users()
    new_user_id = len(data['users']) + 1 # increment id
    new_user = {
        "id": new_user_id,
        "email": email,
        "password": password
    }
    data['users'].append(new_user)
    save_users(data)
    return new_user

# Return the logged in user's ID
def get_logged_in_user():
    user_id = session.get('user_id')
    if user_id:
        return user_id
    else:
        return None

# Functions to validate registration inputs
def validate_email(email):
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_regex, email) is not None

# Ensure password requirements are met
def validate_password(password):
    return len(password) > 0 and len(password) <= 128

# Functions to validate login inputs
def validate_login_email(email):
    valid = True
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    if re.match(email_regex, email) is not None:
        valid = False
    return valid

# Register validation route
@app.route("/api/register", methods = ["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = get_user_by_email(email)

    # Check if user already exists
    if user is not None:
        return jsonify({"msg": "An account with this email already exists"}), 400

    # validate email and password
    if not validate_email(email):
        return jsonify({"msg": "Invalid email"}), 400
    if not validate_password(password):
        return jsonify({"msg": "Invalid password"}), 400

    # if validations pass add user and return success response
    add_user(email, password)
    return jsonify({"msg": "Registration successful"}), 200

# Test login function
@app.route("/api/login", methods = ["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # get user corresponding to email input
    user = get_user_by_email(email)

    # Checks if user exists and if email matches password
    if user is not None:
        if password == user['password']:
            session['user_id'] = user['id']
            return jsonify({"success": True, "msg": "Login successful"}), 200

    return jsonify({"success": False, "msg": "Invalid email or password"}), 401

# To view login route
@app.route("/api/login", methods = ["GET"])
def login_users():
    return "Hello, welcome to login"


### Notification route and functions ###

# Load notifs from json file
def load_notifications():
    with open('dummy/notifications.json', 'r') as file:
        return json.load(file)

def save_notifications(notifications):
    with open('dummy/notifications.json', 'f') as file:
        json.dump(notifications, file, indent=4)

# User notifications page route
@app.route('/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    notifications = load_notifications()
    return jsonify(notifications.get(user_id, []))

def delete_notification(user_id, notification_id):
    notifications  = load_notifications()
    user_notifications = notifications.get(user_id, [])
    notifications[user_id] = [n for n in user_notifications if str(n['id']) != notification_id]
    save_notifications(notifications)


