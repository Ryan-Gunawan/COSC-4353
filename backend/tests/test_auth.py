import unittest
from unittest.mock import patch, mock_open
import sys
sys.path.append('../')
from app import app, db
from routes import validate_email, validate_password, get_user_by_email
from models import User
import json
from flask import Flask, session

# Remember to activate venv for tests to work

class TestUserAuth(unittest.TestCase):

    def setUp(self):
        # Configure Flask app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True

        with app.app_context():
            db.create_all()

    # Clean up after each test
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()


    def test_successful_registration(self):
        response = self.client.post('/api/register',
            json={'email': 'test@example.com',
                  'password': 'ValidPass123!'
                  }
            )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Registration successful')

        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertFalse(user.admin)

    def test_duplicate_email_registration(self):
        # First registration
        self.client.post('/api/register',
            json={
                'email': 'test@example.com',
                'password': 'ValidPass123!'
            }
        )

        # Attempt duplicate registration
        response = self.client.post('/api/register',
            json={
                'email': 'test@example.com',
                'password': 'ValidPass123!'
            }
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'An account with this email already exists')

    def test_invalid_email_registration(self):
        response = self.client.post('/api/register',
            json={
                'email': 'invalid-email',
                'password': 'ValidPass123!'
            }
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Invalid email')

    def test_invalid_password_registration(self):
        response = self.client.post('/api/register',
            json={
                'email': 'test@example.com',
                'password': ''  # password can't be empty
            }
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Invalid password')

    def test_successful_login(self):
            # First register a user
            self.client.post('/api/register',
                json={
                    'email': 'test@example.com',
                    'password': 'ValidPass123!'
                }
            )

            # Then attempt to login
            response = self.client.post('/api/login',
                json={
                    'email': 'test@example.com',
                    'password': 'ValidPass123!'
                }
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertTrue(data['success'])
            self.assertEqual(data['msg'], 'Login successful')

    def test_login_invalid_email(self):
        response = self.client.post('/api/login',
            json={
                'email': 'nonexistent@example.com',
                'password': 'ValidPass123!'
            }
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['msg'], 'Invalid email or password')

    def test_login_wrong_password(self):
        # First register a user
        self.client.post('/api/register',
            json={
                'email': 'test@example.com',
                'password': 'ValidPass123!'
            }
        )

        # Then attempt to login with wrong password
        response = self.client.post('/api/login',
            json={
                'email': 'test@example.com',
                'password': 'WrongPass123!'
            }
        )
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['msg'], 'Invalid email or password')

    def test_login_options_request(self):
        response = self.client.options('/api/login')
        self.assertEqual(response.status_code, 200)

    def test_validate_email(self):
        self.assertTrue(validate_email("email@gmail.com"))
        self.assertTrue(validate_email("EMAIL@YAHOO.COM"))
        self.assertFalse(validate_email("emailgmail.com"))
        self.assertFalse(validate_email("email@gmailcom"))

    def test_validate_password(self):
       self.assertTrue(validate_password("password"))
       self.assertTrue(validate_password("!@PASSWORD12435"))
       self.assertTrue(validate_password("Q#JT\]N~%QaIV|UY3>\O;|U&%ZQwFV?d8rc55z7'H^$@u~+/K4>~oTuxEs\{_{bu.<L*3FvA72xvUn,aedoxR!?52xz&Ln,I0nScGBzO~GL+``Ts1(){tWEB:!j;5>\O"))
       self.assertFalse(validate_password("LQ#JT\]N~%QaIV|UY3>\O;|U&%ZQwFV?d8rc55z7'H^$@u~+/K4>~oTuxEs\{_{bu.<L*3FvA72xvUn,aedoxR!?52xz&Ln,I0nScGBzO~GL+``Ts1(){tWEB:!j;5>\O"))
       self.assertFalse(validate_password(""))


    def test_is_admin(self):
        # Test when session admin is True
        with self.client.session_transaction() as session: # Manually inject session data into flask test client
            session['admin'] = True
        response = self.client.get('/api/isadmin')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'admin': True})

        # Test when session admin is False
        with self.client.session_transaction() as session:
            session['admin'] = False
        response = self.client.get('/api/isadmin')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'admin': False})

if __name__ == '__main__':
    unittest.main()

