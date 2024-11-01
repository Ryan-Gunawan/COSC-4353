from app import app, db
from flask import Flask, request, jsonify, session, redirect, url_for
import json
import re
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, date
# from flask_socketio import SocketIO, emit, join_room

USER_FILE = 'dummy/users.json'

# Needed to periodically check to send reminder notifications
scheduler = BackgroundScheduler()


# Get all users
# Query all users from db and return them as a list
@app.route("/api/users", methods = ["GET"]) # http://localhost/api/users url to see this table
def get_users():
    from app import db
    from models import User

    users = User.query.all()
    result = [user.to_json() for user in users]
    return jsonify(result), 200

@app.route("/api/eventlist", methods = ["GET"])
def get_events():
    from app import db
    from models import Event
    events = Event.query.all()
    result = [event.to_json() for event in events]
    return jsonify(result), 200
    #events = read_events_from_file()
    #return jsonify(events), 200

# This is responsible for editing existing events
@app.route("/api/eventlist/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    from app import db
    from models import Event
    data = request.get_json()
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({"msg": "Event not found"}), 404
    event.name = data.get('name', event.name)
    event.description = data.get('description', event.description)
    event.location = data.get('location', event.location)
    event.skills = data.get('skills', event.skills)
    event.urgency = data.get('urgency', event.urgency)
    event.date = data.get('date', event.date)
    db.session.commit()
    return jsonify({"msg": "Event updated successfully"}), 200

@app.route("/api/eventlist/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    from app import db
    from models import Event
    event = Event.query.get(event_id)
    if event is None:
        return jsonify({"msg": "Event not found"}), 404

    db.session.delete(event)
    db.session.commit()
    return jsonify({"msg": "Event deleted successfully"}), 200

@app.route("/api/newevent", methods = ["POST"])
def post_event():
    from app import db
    from models import Event
    data = request.get_json()
    new_event = Event(
        name=data.get('name'),
        description=data.get('description'),
        location=data.get('location'),
        skills=data.get('skills'),
        urgency=data.get('urgency'),
        date=data.get('date')
    )
    db.session.add(new_event)
    db.session.commit()
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
    from app import db
    from models import User
    user = User.query.filter_by(email=email).first()
    if user:
        return user
        # return {
        #     'id': user.id,
        #     'email': user.email,
        #     'password': user.password,
        #     'admin': user.admin
        # }
    return None
    """
    data = load_users()
    for user in data['users']:
        if user['email'].lower() == email.lower(): # ignore case sensitivity
            return user
    return None
    """

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

# Functions to validate registration inputs
def validate_email(email):
    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(email_regex, email) is not None

# Ensure password requirements are met
def validate_password(password):
    return len(password) > 0 and len(password) <= 128

# Register validation route
@app.route("/api/register", methods = ["POST"])
def register():
    from models import User
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
    # add_user(email, password)
    new_user = User(
        email=email,
        password=password,
        admin=False
    )
    new_user.set_password(password) # hash password
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "Registration successful"}), 200

# Test login function
@app.route("/api/login", methods=["OPTIONS", "POST"])
def login():
    from models import User
    if request.method == "OPTIONS":
        return '', 200

    session.clear()  # Clear any previous sessions, making sure no previous login info

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Get user corresponding to email input
    user = get_user_by_email(email)

    # Checks if user exists and if email matches password
    if user is not None:
        if user.check_password(password): # Compare login pass with hashed pass in db

            # Store user id and admin status in session
            session['user_id'] = user.id
            session['admin'] = user.admin

            print(f"User logged in with ID: {session['user_id']}")
            print(f"Session Data: {session}")

            return jsonify({"success": True, "msg": "Login successful"}), 200
    return jsonify({"success": False, "msg": "Invalid email or password"}), 401

"""# To view login route
@app.route("/api/login", methods = ["GET"])
def login_users():
    return "Hello, welcome to login" """

# Route to get session admin status
@app.route('/api/isadmin', methods=['GET'])
def is_admin():
    if 'admin' in session:
        print(f"User logged in with Admin Status: {session['admin']}")
        return jsonify({"admin": session['admin']}), 200
    return jsonify({"admin": False}), 401# Default to false if admin is not in session

"""@app.route('/api/isadmin', methods=['PUT'])
def update_status():
    # Check if the user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "No user logged in"}), 401
    # Import User model and db inside the function to avoid circular imports
    from models import User
    from app import db
    # Find the user by user_id
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    # Update the 'admin' field to True
    user.admin = True
    # Commit the changes to the database
    db.session.commit()
    return jsonify({"msg": "Admin status updated successfully"}), 200
    """

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
    from app import db
    from models import User, Notification

    user_id = session['user_id']
    if not user_id:
        return jsonify({'msg': 'User not autheniticated'}), 401

    notifications = Notification.query.filter_by(user_id=user_id).all()
    result = [notification.to_json() for notification in notifications]
    return jsonify(result), 200

# Delete notifs from json file
@app.route('/api/notifications', methods=['DELETE'])
def delete_notification():
    from app import db
    from models import Notification

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'msg': 'User not logged in'}), 401

    data = request.get_json()
    notification_id = data.get('notification_id')

    if not notification_id:
        return jsonify({'msg': 'Notification ID is required'}), 400

    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    if not notification:
        return jsonify({'msg': 'Notification not found'}), 404

    db.session.delete(notification)
    db.session.commit()
    return jsonify({'msg': 'Notification deleted successfully'}), 204

# # Sends update to frontend whenever a new notification is added, or if any notifications are unread.
# @app.route('/api/notifications/unread', methods=['GET'])
# def check_unread_notification():
#     user_id = session.get('user_id')
#     if not user_id:
#         return jsonify({'error': 'No user logged in'}), 401
#     notifications = load_notifications()
#     user_notifications = notifications.get(user_id, [])
#     has_unread = any(notification['read'] == False for notification in user_notifications)
#     return jsonify({'has_unread': has_unread})
#
# def has_unread_notificiations(user_id):
#     notifications = load_notifications()
#     user_notifications = notifications.get(user_id, [])
#     return any(notification['read'] == False for notification in user_notifications)


# Send event assignment notification
@app.route('/api/send-assignment-notification', methods=['POST'])
def send_assignment_notification():
    from models import User, Notification
    data = request.get_json()
    user_id = data.get('userId')
    event_name = data.get('eventName')
    event_date = data.get('eventDate')

    # Ensure required fields are present
    if not user_id or not event_name or not event_date:
        return jsonify({'msg': 'user_id, event_name, and event_date are required fields'}), 400

    # Get user from database
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404

    # Create the new notification
    today = date.today()
    current_date = today.strftime("%Y-%m-%d")
    new_notification = Notification(
        user_id = user_id,
        title = "Assignment",
        date = current_date,
        message = "Event assigned: " + event_name + " on " + event_date,
        notif_type = "assignment"
    )

    # add notification to the database
    db.session.add(new_notification)
    db.session.commit()

    print(f"Notification sent to user {user_id} for event '{event_name}'.")
    return jsonify({'msg': 'Notification sent successfully'}), 200

# Sends reminder as event dates approach. Checks daily for upcoming events
# Once we do database consider tracking whether a reminder has been sent for each user and event
# To better handle repeat reminders and timings
def send_reminder_notifications():
    from models import Event, User, Notification

    now = datetime.now()
    reminder_time = now + timedelta(hours=24)

    today = date.today()
    current_date = today.strftime("%m-%d-%y")

    upcoming_events = Event.query.filter(Event.date > now, Event.date <= reminder_time).all()

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
                # socketio.emit('unread_notification', {'has_unread': True}, to=str(user_id))
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
    events = get_events()
    notifications = load_notifications()
    today = date.today()
    current_date = today.strftime("%m-%d-%y")
    event = events[event_id]
    for user_id in event['assignedUsers']:
        new_notification = {
            "id": len(notifications.get(user_id, [])) + 1,
            "title": "Update",
            "date": current_date,
            "message": f"Event Update: '{event['name']}' has been updated, please check the event listing to view any changes.",
            "type": "update",
            "read": False
        }
        notifications[user_id].append(new_notification)
        # socketio.emit('unread_notification', {'has_unread': True}, to=str(user_id))
    save_notifications(notifications)
    print("Sent update")

@app.route("/api/volunteerhistory", methods = ["GET"])
def get_history():
    from app import db
    from models import User, Event
    # session['user_id'] = "1" #manually
    user_id = session['user_id']
    if not user_id:
        return jsonify({'msg': 'User not logged in'}), 401
    # Get volunteer list from user
    user_info = User.query.get(user_id)
    volunteer_info = json.loads(user_info.volunteer)
    # Get event info
    retrieve_event = Event.query.filter(Event.id.in_(volunteer_info)).all()
    event_info = [event.to_json() for event in retrieve_event]

    return jsonify(event_info), 200

@app.route("/api/userprofile", methods = ["GET"])
def get_userinfo():
    from app import db
    from models import User
    # session['user_id'] = "1" #manually

    user_id = session['user_id']
    retrieve = User.query.get(user_id)
    info = retrieve.to_json()
    
    return jsonify(info), 200

@app.route("/api/userprofile/<int:user_id>", methods=["PUT"])
def update_userinfo(user_id):
    from app import db
    from models import User
    # session['user_id'] = "1" #manually

    data = request.get_json()
    retrieve = User.query.get(user_id)
    retrieve.fullname = data.get('fullname', retrieve.fullname)
    retrieve.address1 = data.get('address1', retrieve.address1)
    retrieve.address2 = data.get('address2', retrieve.address2)
    retrieve.city = data.get('city', retrieve.city)
    retrieve.state = data.get('state', retrieve.state)
    retrieve.zipcode = data.get('zipcode', retrieve.zipcode)
    retrieve.skills = data.get('skills', retrieve.skills)
    retrieve.preference = data.get('preference', retrieve.preference)
    retrieve.availability = data.get('availability', retrieve.availability)
    db.session.commit()
    return jsonify({"msg": "User info updated successfully"}), 200


##@app.route("/api/usersList", methods=["GET"])
#def get_userList():
#    from app import db
#    from models import User
    
#    users = User.query.all()
#    lists = [users.to_json() for users in users]

#    return jsonify(lists), 200
#    users = read_users_from_file()
    ##return jsonify(users), 200

##def read_users_from_file():
#   if os.path.exists('dummy/users.json'):
#       with open('dummy/users.json', 'r') as f:
#           return json.load(f)
##    return []


@app.route('/api/match_user', methods=['PUT'])
def match_user():
    from app import db
    # Get JSON data from the request
    data = request.get_json()

    user = data.get('user_id')  # The ID of the user to match
    event = data.get('event_id')  # The ID of the event to match with
    if event is None:
        return jsonify({"msg": "Event not found"}), 404
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    if event not in user.volunteer:
        user.volunteer.append(event)
        db.session.commit()
        return jsonify({"msg": "Event added to volunteer list", "volunteer": user.volunteer}), 200
    else:
        return jsonify({"msg": "Event already in volunteer list", "volunteer": user.volunteer}), 200

    # from models import User, Event
    #
    # # Get JSON data from the request
    # data = request.get_json()
    # user_id = data.get('user_id')  # The ID of the user to match
    # event_id = data.get('event_id')  # The ID of the event to match with
    #
    # if event_id is None:
    #     return jsonify({"msg": "Event ID is required"}), 404
    # if user_id is None:
    #     return jsonify({"msg": "User ID is required"}), 404
    #
    # user = User.query.get(user_id)
    # event = Event.query.get(event_id)
    #
    # if event is None:
    #     return jsonify({"msg": "Event not found"}), 404
    # if user is None:
    #     return jsonify({"msg": "User not found"}), 404
    # 
    # if event_id not in user.volunteer:
    #     user.volunteer.append(event)
    #     db.session.commit()
    # if user not in event.assigned_users:
    #     event.assigned_users.append(user)
    #     db.session.commit()
    #
    #     return jsonify({"msg": "Event added to volunteer list", "volunteer": user.volunteer}), 200
    # else:
    #     return jsonify({"msg": "Event already in volunteer list", "volunteer": user.volunteer}), 200
