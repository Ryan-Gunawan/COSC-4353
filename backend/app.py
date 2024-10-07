from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# users.db is the name of the database, can be renamed later.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///default.db"
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///users.db',
    'events': 'sqlite:///events.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# runs routes.py
import routes

# creates all needed database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
