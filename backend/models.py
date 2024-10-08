from app import db

# Here each class represents objects that will be stored in the database
# and we specify what the attributes are and whether
# they are required or optional.


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    address1 = db.Column(db.String(100), nullable = False)
    address2 = db.Column(db.String(100), nullable = True)
    city = db.Column(db.String(50), nullable = False)
    state = db.Column(db.String(2), nullable = False)
    zip = db.Column(db.Integer, nullable = False)
    # skills
    # preferences
    # availability

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)  # Adjust the length as needed
    location = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(255), nullable=True)  # Adjust the length as needed
    urgency = db.Column(db.String(10), nullable=True)  # e.g., "HIGH", "MEDIUM", "LOW"
    date = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "skills": self.skills,
            "urgency": self.urgency,
            "date": self.date.isoformat() if self.date else None  # Format date as string
        }


# Converts objects to json for client to store in db
# Probably need to edit to be able to convert any type of object (User or Event)
def to_json(self):
    return {
        "id":self.id
        # continue... later
    }
