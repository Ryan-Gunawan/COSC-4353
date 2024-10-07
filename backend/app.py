from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

app.secret_key = 'secretkey' # Required for sessions

# users.db is the name of the database, can be renamed later.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None' # required for cross-site requests. When using diff ports
app.config['SESSION_COOKIE_SECURE'] = False # True if using HTTPS
app.config['SECRET_KEY'] = 'secretkey' # required for sessions
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
#app.config['SESSION_TYPE'] = 'filesystem' # use filesystem-based sessions

# Session(app)

db = SQLAlchemy(app)

# runs routes.py
import routes

# creates all needed database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
