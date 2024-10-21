import os
import json
from datetime import datetime
from app import app, db, Event  # Assuming Event is your model and db is initialized


script_dir = os.path.dirname(__file__)
events_file_path = os.path.join(script_dir, 'dummy', 'events.json')
# Load JSON data
with open(events_file_path) as f:
    events_data = json.load(f)

# Iterate over each user in the JSON file
def parse_date(date_str):
    try:
        # Try parsing with time first
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        # If that fails, try just the date
        return datetime.strptime(date_str, "%Y-%m-%d")

with app.app_context():
    # Iterate over the event data
    for event_data in events_data:
        # Parse the date using the custom parse_date function
        event_date = parse_date(event_data['date'])

        # Create a new Event object with default values for missing fields
        new_event = Event(
            name=event_data['name'],
            description=event_data.get('description', ""),  # Default to empty string if missing
            location=event_data['location'],
            skills=json.dumps(event_data.get('skills', [])),  # Convert list to JSON string
            urgency=event_data.get('urgency', "MEDIUM"),  # Default to "MEDIUM" if urgency is missing
            date=event_date
        )

        # Add the event to the session
        db.session.add(new_event)

    # Commit all the new events to the database
    db.session.commit()

print(f"{len(events_data)} events added to the database.")