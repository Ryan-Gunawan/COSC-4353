from app import app, db
from flask import Flask, request, jsonify, session, redirect, url_for, send_file, Blueprint, Response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
import json
import re
import os
import csv
from io import BytesIO, StringIO
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, date

USER_FILE = 'dummy/users.json'

# Needed to periodically check to send reminder notifications
scheduler = BackgroundScheduler()

# To get report type from front end
report_bp = Blueprint('report_bp', __name__)

def generate_csv_report():
    from models import User, Event

    # Check if the user is an admin
    if not is_admin():
        return jsonify({"success": False, "msg": "Unauthorized access"}), 403

    # Create a CSV in memory
    csv_output = StringIO()
    csv_writer = csv.writer(csv_output)

    # Write the headers to the CSV file
    csv_writer.writerow(['Volunteer Activity and Event Management Report'])
    csv_writer.writerow([''])

    # Volunteer Participation History
    csv_writer.writerow(['1. Volunteer Participation History'])
    csv_writer.writerow(['Name', 'Email', 'Events'])
    
    users = User.query.all()
    for user in users:
        events_list = []
        for event in user.events:
            events_list.append(f"{event.name} on {event.date}")
        events_str = ", ".join(events_list) if events_list else "No participation history"
        csv_writer.writerow([user.fullname, user.email, events_str])
    
    csv_writer.writerow([''])
    
    # Event List with Volunteer Assignments
    csv_writer.writerow(['2. Event List with Volunteer Assignments'])
    csv_writer.writerow(['Event Name', 'Date', 'Location', 'Description', 'Skills', 'Assigned Volunteers'])
    
    events = Event.query.all()
    for event in events:
        # Format skills
        if event.skills:
            try:
                skills_list = json.loads(event.skills)
                skills_str = ", ".join(skills_list)
            except json.JSONDecodeError:
                skills_str = event.skills  # Fallback if skills are not in valid JSON format
        else:
            skills_str = "No skills available"

        # Get assigned volunteers
        if event.assigned_users:
            assigned_volunteers = ", ".join([f"{user.fullname} ({user.email})" for user in event.assigned_users])
        else:
            assigned_volunteers = "None"

        # Write event details to CSV
        csv_writer.writerow([event.name, event.date, event.location, event.description, skills_str, assigned_volunteers])

    # Reset the cursor of the StringIO buffer
    csv_output.seek(0)

    # Return the CSV as a downloadable file
    return Response(
        csv_output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=full_report.csv'}
    )

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

    # Send update notifications to all assigned users
    send_event_update_notifications(event_id)
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

# Function to get user by email
def get_user_by_email(email):
    from app import db
    from models import User
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    return None

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

    # Clear prev session data
    session.pop("user_id", None)
    session.pop("admin", None)
    session.clear()

    # print("cleared session")
    # print(f"Session ID: {session['user_id']}")
    # print(f"Admin status: {session['admin']}")

    # Check if user already exists
    user = get_user_by_email(email)
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

            if not user.profile_setup:
                profile_setup = False
                user.profile_setup = True
                db.session.commit()
            else:
                profile_setup = True

            print(f"User logged in with ID: {session['user_id']}")
            print(f"Session Data: {session}")

            return jsonify({"success": True, "profile_setup": profile_setup, "msg": "Login successful"}), 200
    return jsonify({"success": False, "msg": "Invalid email or password"}), 401

# Route to get session admin status
@app.route('/api/isadmin', methods=['GET'])
def is_admin():
    if 'admin' in session:
        print(f"User logged in with Admin Status: {session['admin']}")
        return jsonify({"admin": session['admin']}), 200
    return jsonify({"admin": False}), 401# Default to false if admin is not in session


### Notification route and functions ###

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

# Helper function to create assignment notification
def create_assignment_notification(user_id, event_name, event_date):
    from models import User, Notification
    user = User.query.get(user_id)
    if not user:
        print(f"User with ID {user_id} not found.")
        return False

    # Create and add notification to db
    today = date.today()
    current_date = today.strftime("%Y-%m-%d")
    new_notification = Notification(
        user_id=user_id,
        title="Assignment",
        date=current_date,
        message=f"Event assigned: {event_name} on {event_date}",
        notif_type="assignment"
    )
    db.session.add(new_notification)
    db.session.commit()
    print(f"Notification sent to user {user_id} for event '{event_name}'.")
    return True

# Send event assignment notification. Route used for testing sending notifications.
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

    # Use the helper function to create the notification
    if create_assignment_notification(user_id, event_name, event_date):
        return jsonify({'msg': 'Notification sent successfully'}), 200
    else:
        return jsonify({'msg': 'User not found'}), 404

# Sends reminder as event dates approach. Checks daily for upcoming events
def send_reminder_notifications():
    from models import Event, User, Notification
    from app import app

    with app.app_context():
        now = datetime.now()
        today = date.today()
        tomorrow = today + timedelta(days=1)
        current_date = today.strftime("%m-%d-%Y")

        # Query events happening tomorrow
        upcoming_events = Event.query.filter(
            Event.date >= tomorrow,
            Event.date < tomorrow + timedelta(days=1)
        ).all()

        # Print the current time and upcoming events for debugging
        # print(f"Current time: {today}, Tomorrow: {tomorrow}")
        # print(f"Found upcoming events: {[event.name for event in upcoming_events]}")  # Print event names

        for event in upcoming_events:
            # event_date = datetime.strptime(event.date, '%Y-%m-%dT%H:%M:%S') if 'T' in event.date else datetime.strptime(event.date, '%Y-%m-%d')
            # print(f"Today: {today}, Event date: {event_date.date()}, Tomorrow: {tomorrow}")    try:
            try:
                if 'T' in event.date:
                    # Try to parse with seconds, if it fails, fall back to just hours and minutes
                    try:
                        event_date = datetime.strptime(event.date, '%Y-%m-%dT%H:%M:%S')
                    except ValueError:
                        event_date = datetime.strptime(event.date, '%Y-%m-%dT%H:%M')
                else:
                    event_date = datetime.strptime(event.date, '%Y-%m-%d')

                if today < event_date.date() <= tomorrow:
                    if event.assigned_users:
                        for user in event.assigned_users:
                            new_notification = Notification(
                                user_id = user.id,
                                title = "Reminder",
                                date = current_date,
                                message = f"Event reminder: {event.name} is coming up in 24 hours!",
                                notif_type = "reminder"
                            )
                            db.session.add(new_notification)
                            print(f"Appended notification successfully to user: {user.id}")
                        db.session.commit()
                    else:
                        print(f"No assigned users for event '{event.name}'")
            except ValueError as e:
                print(f"Failed to parse event date for event '{event.name}': {event.date}. Error: {e}")

# Set up scheduler to periodically check to send reminder notifications
# To test make sure event is set to next day not same day
if not scheduler.get_job('reminder_notifications'):
    scheduler.add_job(send_reminder_notifications, 'interval', hours=10, id='reminder_notifications')
scheduler.start()

# When admin updates an event all the assigned users are sent an update notification
# may need to change to use a route: get request data with event_id
def send_event_update_notifications(event_id):
    from models import Event, User, Notification
    today = date.today()
    current_date = today.strftime("%Y-%m-%d")
    event = Event.query.get(event_id)
    if not event.assigned_users:
        print("No users assigned to this event.")
        return
    for user in event.assigned_users:
        new_notification = Notification(
            user_id = user.id,
            title = "Update",
            date = current_date,
            message = f"Event update: '{event.name}' has been updated. Please check the event listing to view any changes.",
            notif_type = "update"
        )
        db.session.add(new_notification)
        print(f"Appended notification successfully to user: {user.id}")
    db.session.commit()
    print(f"Sent update notifications for event: {event.name}")

@app.route("/api/volunteerhistory", methods = ["GET"])
def get_history():
    from app import db
    from models import User, Event

    # session['user_id'] = "1" #manually
    user_id = session['user_id']
    if not user_id:
        return jsonify({'msg': 'User not logged in'}), 401
    user = User.query.get(user_id)
    volunteer_history = user.events
    event_info = [event.to_json() for event in volunteer_history]

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
    from models import User, Event

    # Get JSON data from the request
    data = request.get_json()
    user_id = data.get('user_id')  # The ID of the user to match
    event_id = data.get('event_id')  # The ID of the event to match with

    if event_id is None:
        return jsonify({"msg": "Event ID is required"}), 404
    if user_id is None:
        return jsonify({"msg": "User ID is required"}), 404

    user = User.query.get(user_id)
    event = Event.query.get(event_id)

    if event is None:
        return jsonify({"msg": "Event not found"}), 404
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    if user not in event.assigned_users:
        event.assigned_users.append(user) # automatically appends to user.volunteer since they're connected on db
        db.session.commit()

        # Send assignment notification to user
        if create_assignment_notification(user_id, event.name, event.date):
            return jsonify({"msg": "Event added to volunteer list and notification sent"}), 200
        else:
            return jsonify({"msg": "Event added to volunteer list, but failed to send notification"}), 200
    else:
        return jsonify({"msg": "Event already in volunteer list"}), 200

@report_bp.route('/api/generate_report', methods=['GET'])
def generate_report():
    report_type = request.args.get('type') # get tpe pdf or csv from frontend query

    if report_type == "pdf":
        return generate_pdf_report()
    elif report_type == "csv":
        return generate_csv_report()
        # return jsonify({"success": False, "msg": "Invalid report type csv"}), 400
    else:
        return jsonify({"success": False, "msg": "Invalid report type"}), 400

def generate_pdf_report():
    from models import User, Event

    if not is_admin():
        return jsonify({"success": False, "msg": "Unauthorized access"}), 403

    def wrap_text(text, max_width):
        """Helper function to wrap text within a specified width."""
        lines = []
        words = text.split(' ')
        line = ''
        for word in words:
            if canvas_obj.stringWidth(line + word, "Helvetica", 10) < max_width:
                line += f"{word} "
            else:
                lines.append(line)
                line = f"{word} "
        lines.append(line)  # Add the last line
        return lines

    # Create a PDF file in memory
    pdf_buffer = BytesIO()
    canvas_obj = canvas.Canvas(pdf_buffer, pagesize=letter)
    canvas_obj.setTitle("Volunteer Activity and Event Management Report")

    # Adjust margins
    left_margin = 50
    right_margin = 540  # page width (612) - 72 margin
    content_width = right_margin - left_margin

    # Title - Centered
    title = "Volunteer Activity and Event Management Report"
    title_width = canvas_obj.stringWidth(title, "Helvetica-Bold", 16)
    canvas_obj.setFont("Helvetica-Bold", 16)
    canvas_obj.drawString((612 - title_width) / 2, 750, title)  # Center the title

    canvas_obj.setFont("Helvetica", 12)  # Set default font back to regular

    # Move the dividing line above the "1. Volunteer Participation History" header
    canvas_obj.setStrokeColor(colors.black)
    canvas_obj.setLineWidth(1)
    canvas_obj.line(left_margin, 725, right_margin, 725)  # Line above the first section header

    # Section 1 Header: Volunteer Participation History (Bold)
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawString(left_margin, 710, "Volunteer Participation History")
    canvas_obj.setFont("Helvetica", 12)  # Reset to regular font

    y_position = 690
    users = User.query.all()
    user_counter = 1  # Counter for numbering users
    for user in users:
        canvas_obj.drawString(left_margin, y_position, f"{user_counter}. Name: {user.fullname}, Email: {user.email}")
        y_position -= 20

        events = user.events
        if events:
            # Add the 'Events:' label before listing events
            canvas_obj.drawString(left_margin + 20, y_position, "Events:")
            y_position -= 20
            for event in events:
                # Event name and right-aligned date
                canvas_obj.drawString(left_margin + 40, y_position, f"- {event.name}")
                canvas_obj.drawRightString(right_margin, y_position, f"{event.date}")
                y_position -= 20
        else:
            canvas_obj.drawString(left_margin + 20, y_position, "No participation history.")
            y_position -= 20
        y_position -= 10

        user_counter += 1  # Increment user counter

        # If the page gets filled, create a new one
        if y_position < 50:
            canvas_obj.showPage()
            y_position = 750

    # Draw a dividing line before section 2
    y_position -= 10  # Adjust to ensure the line doesn't overlap the content
    canvas_obj.line(left_margin, y_position, right_margin, y_position)  # One line between sections

    # Section 2 Header: Event List with Volunteer Assignments (Bold)
    y_position -= 20  # Add space after the line before the next header
    canvas_obj.setFont("Helvetica-Bold", 12)
    canvas_obj.drawString(left_margin, y_position, "Event List with Volunteer Assignments")
    canvas_obj.setFont("Helvetica", 12)  # Reset to regular font

    # Space after the second header
    y_position -= 20  # Ensure enough space before the content starts

    y_position -= 10  # Adjust space before the content starts
    events = Event.query.all()
    event_counter = 1  # Counter for numbering events
    for event in events:
        # Number each event
        canvas_obj.drawString(left_margin, y_position, f"{event_counter}. Event: {event.name}")
        canvas_obj.drawRightString(right_margin, y_position, f"{event.date}")
        y_position -= 20

        canvas_obj.drawString(left_margin + 20, y_position, f"Location: {event.location}")
        y_position -= 20

        # Parse the JSON string into a list
        if event.skills:
            try:
                skills_list = json.loads(event.skills)
                # Join the list into a comma-separated string
                skills_str = ", ".join(skills_list)
            except json.JSONDecodeError:
                skills_str = event.skills  # Fallback in case the JSON is malformed
        else:
            skills_str = "No skills available"  # Fallback if there are no skills

        # Now print the skills
        canvas_obj.drawString(left_margin + 20, y_position, f"Skills: {skills_str}")
        y_position -= 20

        # Wrap description text
        description_lines = wrap_text(event.description, content_width)
        canvas_obj.drawString(left_margin + 20, y_position, "Description: ")  # Add the 'Description:' label
        y_position -= 15

        # Print the wrapped description text
        for line in description_lines:
            canvas_obj.drawString(left_margin + 40, y_position, line)  # Indent the wrapped lines
            y_position -= 15

        if event.assigned_users:
            canvas_obj.drawString(left_margin + 20, y_position, "Assigned Volunteers:")
            y_position -= 20
            for user in event.assigned_users:
                canvas_obj.drawString(left_margin + 40, y_position, f"- {user.fullname} ({user.email})")
                y_position -= 20
        else:
            canvas_obj.drawString(left_margin + 20, y_position, "Assigned Volunteers: None")
            y_position -= 20

        y_position -= 30

        event_counter += 1  # Increment event counter

        # If the page gets filled, create a new one
        if y_position < 50:
            canvas_obj.showPage()
            y_position = 750

    canvas_obj.save()
    pdf_buffer.seek(0)

    return send_file(pdf_buffer, as_attachment=True, download_name="full_report.pdf", mimetype='application/pdf')

app.register_blueprint(report_bp)
