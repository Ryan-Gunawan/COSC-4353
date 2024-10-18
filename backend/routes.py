from app import app, db
from flask import Flask, request, jsonify, session, redirect, url_for
import json
from models import User, Event
import re
import os
from datetime import datetime

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
    #events = Event.query.all() This is for when the database is implemented
    #result = [event.to_json() for event in events]
    #return jsonify(result), 200
    events = read_events_from_file()
    return jsonify(events), 200
def read_events_from_file():
    if os.path.exists('dummy/events.json'):
        with open('dummy/events.json', 'r') as f:
            return json.load(f)  # Directly return the loaded list
    return [] # Return an empty list if the file does not exist
def add_events_to_file(events):
    with open('dummy/events.json', 'w') as f:
        json.dump(events, f, indent=4)

# This is responsible for editing existing events
@app.route("/api/eventlist/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    data = request.get_json()
    events = read_events_from_file()
    for event in events:
        if event['id'] == event_id:
            event.update(data)
            break
    add_events_to_file(events)
    return jsonify({"msg": "Event updated successfully"}), 200

@app.route("/api/eventlist/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    events = read_events_from_file()
    event_to_delete = next((event for event in events if event['id'] == event_id), None)

    if event_to_delete is None:
        return jsonify({"msg": "Event not found"}), 404

    events = [event for event in events if event['id'] != event_id]
    add_events_to_file(events)
    return jsonify({"msg": "Event deleted successfully"}), 200

@app.route("/api/newevent", methods = ["POST"])
def post_event():
    data = request.get_json()
    print(data)
    events = read_events_from_file()
    events.append(data)
    add_events_to_file(events)
    return jsonify({"msg": "Event created successfully"}), 201

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
        "password": password,
        "admin": False
    }
    data['users'].append(new_user)
    save_users(data)
    return new_user

# Return the logged in user's ID
def get_logged_in_user():
    user_id = session['user_id']
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
            session['user_id'] = user['id'] # Store user ID in session
            session['admin'] = user['admin'] # Store user admin status in session
            print(f"User logged in with ID: {session['user_id']}")
            print(f"User logged in with Admin Status: {session['admin']}")
            return jsonify({"success": True, "msg": "Login successful"}), 200

    return jsonify({"success": False, "msg": "Invalid email or password"}), 401

# To view login route
@app.route("/api/login", methods = ["GET"])
def login_users():
    return "Hello, welcome to login"

# Route to get session admin status
@app.route('/api/isadmin', methods=['GET'])
def is_admin():
    if 'admin' in session:
        print(f"User logged in with Admin Status: {session['admin']}")
        return jsonify({"admin": session['admin']}), 200

    return jsonify({"admin": False}), 200# Default to false if admin is not in session


### Notification route and functions ###

# Load notifs from json file
def load_notifications():
    with open('dummy/notifications.json', 'r') as file:
        return json.load(file)

# Saves notifs to json file
def save_notifications(notifications):
    with open('dummy/notifications.json', 'w') as file:
        json.dump(notifications, file, indent=4)

# Get all user notifications
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    #print(request.headers) # Log request headers
    user_id = session['user_id']
    print(f"User ID from session: {user_id}")
    if not user_id:
        return jsonify({'msg': 'User not logged in'}), 401
    notifications = load_notifications()
    return jsonify(notifications.get(user_id, []))

# Delete notifs from json file
@app.route('/api/notifications', methods=['DELETE'])
def delete_notification():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'msg': 'User not logged in'}), 401

    data = request.get_json()
    notification_id = data.get('notification_id')

    if not notification_id:
        return jsonify({'msg': 'Notification ID is required'}), 400

    notifications = load_notifications()
    user_notifications = notifications.get(user_id, [])
    notifications[user_id] = [n for n in user_notifications if str(n['id']) != notification_id]

    save_notifications(notifications)
    return '', 204

# Adds notifications to user
@app.route('/api/notifications', methods=['POST'])
def add_notification(user_id):
    notifications = load_notifications()
    new_notification = request.json
    if user_id in notifications:
        notifications[user_id].append(new_notification)
    else:
        notifications[user_id] = [new_notification]
    save_notifications(notifications)
    return jsonify(new_notification), 201

@app.route("/api/volunteerhistory", methods = ["GET"])
def get_history():
    # session['user_id'] = "1" #manually
    user_id = session['user_id']
    if not user_id:
        return jsonify({'msg': 'User not logged in'}), 401
    history = []
    if os.path.exists('dummy/history.json'):
        with open('dummy/history.json', 'r') as f:
            history = json.load(f)
    return jsonify(history.get(user_id, [])), 200

@app.route("/api/userprofile", methods = ["GET"])
def get_userinfo():
    # session['user_id'] = "1" #manually
    user_id = session['user_id']
    if not user_id:
        return jsonify({'msg': 'User not logged in'}), 401
    info = []
    if os.path.exists('dummy/userinfo.json'):
        with open('dummy/userinfo.json', 'r') as f:
            info = json.load(f)
    return jsonify(info.get(user_id, [])), 200

@app.route("/api/userprofile/<int:user_id>", methods=["PUT"])
def update_userinfo(user_id):
    data = request.get_json()
    old_data = []

    # Get old data
    if os.path.exists('dummy/userinfo.json'):
        with open('dummy/userinfo.json', 'r') as f:
            old_data = json.load(f)

    if str(user_id) in old_data:
        user_info = old_data[str(user_id)][0]  # Access the first object in the list
        user_info.update(data)  # Update the user info
    
    # Write data into json
    with open('dummy/userinfo.json', 'w') as f:
        json.dump(old_data, f, indent=4)
    return jsonify({"msg": "User info updated successfully"}), 200