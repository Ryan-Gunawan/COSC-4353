from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

app.secret_key = 'secretkey' # Required for sessions

# users.db is the name of the database, can be renamed later.
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///default.db"
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'sqlite:///users.db',
    'events': 'sqlite:///events.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # Allows cookies to be sent during local dev
app.config['SESSION_COOKIE_SECURE'] = False #  Allows cookies to be sent over HTTP without security
app.config['SESSION_COOKIE_DOMAIN'] = None # Allows both localhost and 127.0.0.1 to work

# In production use these settings:
# app.config['SESSION_COOKIE_SAMESITE'] = 'None' # required for cross-site requests. When using diff ports
# app.config['SESSION_COOKIE_SECURE'] = True # True if using HTTPS

# Other optional settings I was messing with. I don't think we need these, but just in case I'll keep them here for a bit
# app.config['SECRET_KEY'] = 'secretkey' # required for sessions
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
# app.config['SESSION_TYPE'] = 'filesystem' # use filesystem-based sessions
# Session(app)

db = SQLAlchemy(app)

# runs routes.py
import routes

# creates all needed database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
