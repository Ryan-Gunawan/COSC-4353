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
    city = db.Column(db.String(2), nullable = False)
    zip = db.Column(db.Integer, nullable = False)
    # skills
    # preferences
    # availability

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # description
    # location
    # required_skills
    # urgency
    # date


# Converts objects to json for client to store in db
# Probably need to edit to be able to convert any type of object (User or Event)
def to_json(self):
    return {
        "id":self.id,
        # continue... later
    }
