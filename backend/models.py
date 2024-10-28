from app import db
import bcrypt
from sqlalchemy.types import JSON, Text
import json

# Here each class represents objects that will be stored in the database as tables
# and we specify what the attributes are and whether
# they are required or optional.


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}  # Avoid redefining the table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # In practice, store hashed passwords
    admin = db.Column(db.Boolean, default=False)
    fullname = db.Column(db.String(100), nullable=True)
    address1 = db.Column(db.String(100), nullable=True)
    address2 = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zipcode = db.Column(db.String(5), nullable=True)
    skills = db.Column(JSON, nullable=True)
    preference = db.Column(db.String(255), nullable=True)
    availability = db.Column(JSON, nullable=True)
    volunteer = db.Column(JSON, nullable=True)

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "fullname": self.fullname,
            "address1": self.address1,
            "address2": self.address2 or "",
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "skills": self.skills if self.skills else [],
            "preference": self.preference or "",
            "availability": self.availability if self.availability else [],
            "volunteer": self.volunteer if self.volunteer else [],
            "admin": self.admin
        }

    # Has the password with bcrypt and store it
    def set_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed_password.decode('utf-8')

    # Check if password provided at login matched the stored hashed password
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    def __repr__(self):
        return f"<User {self.fullname}>"

class Event(db.Model):
    __tablename__ = 'event'
    __table_args__ = {'extend_existing': True}  # Add this line to avoid redefining the table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)  # Adjust the length as needed
    location = db.Column(db.String(100), nullable=False)
    skills = db.Column(Text, nullable=True)  # Store as a JSON string
    urgency = db.Column(db.String(10), nullable=True)  # e.g., "HIGH", "MEDIUM", "LOW"
    date = db.Column(db.DateTime, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "skills": json.loads(self.skills) if self.skills else [],
            "urgency": self.urgency,
            "date": self.date.isoformat() if self.date else None  # Format date as string
        }

