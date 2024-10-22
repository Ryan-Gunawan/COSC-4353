import os
import json
from datetime import datetime
from app import app, db, User  # Assuming Event is your model and db is initialized


script_dir = os.path.dirname(__file__)
users_file_path = os.path.join(script_dir, 'dummy', 'users.json')
# Load JSON data
with open(users_file_path) as f:
    users_data = json.load(f)

# Iterate over each user in the JSON file
with app.app_context():
    for user_data in users_data:
        # Create a new User object and handle missing keys with .get()
        new_user = User(
            email=user_data.get('email'),  # If email is missing, this will throw an error, so ensure it's present
            password=user_data.get('password', 'defaultpassword'),  # Provide a default password if missing
            admin=user_data.get('admin', False),  # Default to False if 'admin' is missing
            fullname=user_data.get('fullname', ""),  # Default to empty string if 'fullname' is missing
            address1=user_data.get('address1', ""),  # Default to empty string if 'address1' is missing
            address2=user_data.get('address2', None),  # Default to None if 'address2' is missing
            city=user_data.get('city', ""),  # Default to empty string if 'city' is missing
            state=user_data.get('state', ""),  # Default to empty string if 'state' is missing
            zipcode=user_data.get('zipcode', ""),  # Default to empty string if 'zipcode' is missing
            
            # Serialize the skills, availability, and volunteer fields as JSON strings
            skills=json.dumps(user_data.get('skills', [])),  # Default to an empty list if 'skills' is missing
            preference=user_data.get('preference', ""),  # Default to empty string if 'preference' is missing
            availability=json.dumps(user_data.get('availability', [])),  # Default to an empty list if 'availability' is missing
            volunteer=json.dumps(user_data.get('volunteer', []))  # Default to an empty list if 'volunteer' is missing
        )

        # Add the new user to the session
        db.session.add(new_user)

    # Commit all the new users to the database
    db.session.commit()

print(f"{len(users_data)} users added to the database.")