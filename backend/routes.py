from app import app, db, socketio
from flask import Flask, request, jsonify, session, redirect, url_for
import json
from models import User, Event
import re
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, date
from flask_socketio import SocketIO, emit, join_room

USER_FILE = 'dummy/users.json'

# Needed to periodically check to send reminder notifications
scheduler = BackgroundScheduler()


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


### Login and Registration Routes and Functions ###

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

# I don't think we even use this. Just get the session user_id within whatever function needs it
# Return the logged in user's ID
# @app.route("/api/getloggedinuser", methods = ["GET"])
# def get_logged_in_user():
#     user_id = session['user_id']
#     if user_id:
#         return user_id
#     else:
#         return None

# Functions to validate registration inputs
def validate_email(email):
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_regex, email) is not None

# Ensure password requirements are met
def validate_password(password):
    return len(password) > 0 and len(password) <= 128

# Functions to validate login inputs
# I think this is not even used?
# def validate_login_email(email):
#     valid = True
#     email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
#     if re.match(email_regex, email) is not None:
#         valid = False
#     return valid

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
    # Delete "id" or id, string and int ids. Once we get database we can remove the string check
    notifications[user_id] = [n for n in user_notifications if str(n['id']) != notification_id]
    notifications[user_id] = [n for n in user_notifications if n['id'] != notification_id]

    save_notifications(notifications)

    # check if there are any remaining unread notifs and emit to frontend
    has_unread = has_unread_notificiations(user_id)
    socketio.emit('unread_notification', {'has_unread': has_unread}, to=str(user_id))

    return jsonify({'msg': 'Notification deleted successfully'}), 204

# # Sends update to frontend whenever a new notification is added, or if any notifications are unread.
@app.route('/api/notifications/unread', methods=['GET'])
def check_unread_notification():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No user logged in'}), 401
    notifications = load_notifications()
    user_notifications = notifications.get(user_id, [])
    has_unread = any(notification['read'] == False for notification in user_notifications)
    return jsonify({'has_unread': has_unread})

def has_unread_notificiations(user_id):
    notifications = load_notifications()
    user_notifications = notifications.get(user_id, [])
    return any(notification['read'] == False for notification in user_notifications)


# Send event assignment notification
@app.route('/api/send-assignment-notification', methods=['POST'])
def send_assignment_notification():
    data = request.get_json()
    user_id = data.get('userId')
    event_name = data.get('eventName')
    event_date = data.get('eventDate')

    if not user_id or not event_name or not event_date:
        return jsonify({'msg': 'user_id, event_name, and event_date are required fields'}), 400

    notifications = load_notifications()

    # Check if the user_id exists in the notifications, if not, create an empty list
    if user_id not in notifications:
        notifications[user_id] = []

    today = date.today()
    current_date = today.strftime("%Y-%m-%d")

    new_notification = {
        "id": len(notifications[user_id]) + 1,  # Increment notification ID for the user
        "title": "Assignment",
        "date": current_date,
        "message": "Event assigned: " + event_name + " on " + event_date,
        "type": "assignment",
        "read": False
    }

    # Append the new notification to the user's notification list
    notifications[user_id].append(new_notification)

    # Save the updated notifications
    save_notifications(notifications)

    socketio.emit('unread_notification', {'has_unread': True}, to=str(user_id))

    print(f"Notification sent to user {user_id} for event '{event_name}'.")
    return jsonify({'msg': 'Notification sent successfully'}), 200

# Sends reminder as event dates approach. Checks daily for upcoming events
# Once we do database consider tracking whether a reminder has been sent for each user and event
# To better handle repeat reminders and timings
def send_reminder_notifications():
    events = read_events_from_file()
    notifications = load_notifications()

    now = datetime.now()
    reminder_time = now + timedelta(hours=24)

    today = date.today()
    current_date = today.strftime("%m-%d-%y")

    for event in events:
        try:
            event_date = datetime.strptime(event['date'], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')

        if now < event_date <= reminder_time:
            for user_id in event['assignedUsers']:
                new_notification = {
                    "id": len(notifications.get(user_id, [])) + 1,
                    "title": "Reminder",
                    "date": current_date,
                    "message": f"Event Reminder: '{event['name']}' is coming up in 24 hours!",
                    "type": "reminder",
                    "read": False
                }
                notifications[user_id].append(new_notification)
                socketio.emit('unread_notification', {'has_unread': True}, to=str(user_id))
                print("Appended notification successfully")
    save_notifications(notifications)
    print("Sent reminders for upcoming events")

# Set up scheduler to periodically check to send reminder notifications
# To test make sure event is set to next day not same day
if not scheduler.get_job('reminder_notifications'):
    scheduler.add_job(send_reminder_notifications, 'interval', hours=24, id='reminder_notifications')
scheduler.start()

# When admin updates an event all the assigned users are sent an update notification
# may need to change to use a route: get request data with event_id
def send_event_update_notifications(event_id):
    events = read_events_from_file()
    notifications = load_notifications()
    today = date.today()
    current_date = today.strftime("%m-%d-%y")
    event = events[event_id]
    for user_id in event['assignedUsers']:
        new_notification = {
            "id": len(notifications.get(user_id, [])) + 1,
            "title": "Update",
            "date": current_date,
            "message": f"Event Update: '{event['name']}' s been updated, please check the event listing to view any changes.",
            "type": "update",
            "read": False
        }
        notifications[user_id].append(new_notification)
        socketio.emit('unread_notification', {'has_unread': True}, to=str(user_id))
    save_notifications(notifications)
    print("Sent update")

@app.route("/api/volunteerhistory", methods = ["GET"])
def get_history():
    # session['user_id'] = "1" #manually
    user_id = session['user_id']
    if not user_id:
        return jsonify({'msg': 'User not logged in'}), 401
    
    # Get volunteerhistory from users
    history = []
    if os.path.exists('dummy/users.json'):
        with open('dummy/users.json', 'r') as f:
            data = json.load(f)
            users_info = data.get('users', [])
            
    for user in users_info:
        if user['id'] == user_id:
            history = user.get('volunteer', [])
            break
    
    # Get event info from databases
    event_data = []
    if os.path.exists('dummy/events.json'):
        with open('dummy/events.json', 'r') as f:
            event_data = json.load(f)
    
 
    event_info = []
    job = 0
    for event in event_data:
        if job < len(history) and event['id'] == history[job]:
            event_info.append(event)
            job += 1

    return jsonify(event_info), 200

@app.route("/api/userprofile", methods = ["GET"])
def get_userinfo():
    # session['user_id'] = "2" #manually
    user_id = session['user_id']
    if not user_id:
        return jsonify({'msg': 'User not logged in'}), 401
    info = []
    if os.path.exists('dummy/users.json'):
        with open('dummy/users.json', 'r') as f:
            data = json.load(f)
            users_info = data.get('users', [])
            
            for user in users_info:
                if user['id'] == user_id:
                    info.append(user) #Return as array
                    break

    return jsonify(info), 200

@app.route("/api/userprofile/<int:user_id>", methods=["PUT"])
def update_userinfo(user_id):
    data = request.get_json()
    old_data = []

    # Get old data
    if os.path.exists('dummy/users.json'):
        with open('dummy/users.json', 'r') as f:
            old_data = json.load(f)

    users = old_data.get('users', [])

    for user in users:
        if user['id'] == str(user_id):
            user.update(data)
    
    # Write data into json
    with open('dummy/users.json', 'w') as f:
        json.dump(old_data, f, indent=4)
        
    return jsonify({"msg": "User info updated successfully"}), 200



@app.route("/api/usersList", methods=["GET"])
def get_userList():
    users = read_users_from_file()
    return jsonify(users), 200

def read_users_from_file():
    if os.path.exists('dummy/users.json'):
        with open('dummy/users.json', 'r') as f:
            return json.load(f)
    return []


@app.route('/api/match_user', methods=['POST'])
def match_user():
    # Get JSON data from the request
    data = request.get_json()

    user_id = data.get('user_id')  # The ID of the user to match
    event_id = data.get('event_id')  # The ID of the event to match with

    # Load user data from the JSON file
    with open('dummy/users.json', 'r') as f:
        users_data = json.load(f)

    # Find the user by ID
    user_found = False
    for user in users_data['users']:
        if user['id'] == user_id:
            # Check if the user is already matched to the event
            if event_id in user.get('volunteer', []):
                return jsonify({'message': 'Volunteer has already been matched to this event.'}), 400

            # Add event ID to volunteer array
            user.setdefault('volunteer', []).append(event_id)
            user_found = True
            break

    if not user_found:
        return jsonify({'message': 'User not found.'}), 404

    # Save the updated user data back to the JSON file
    with open('dummy/users.json', 'w') as f:
        json.dump(users_data, f, indent=4)

    return jsonify({'message': 'User matched successfully!'}), 200

@socketio.on('join')
def on_join():
    user_id = session.get('user_id')
    if user_id:
        join_room(user_id)
        print(f"User {user_id} has joined room {user_id}")
    else:
        print("No user_id in session. User is not logged in.")
