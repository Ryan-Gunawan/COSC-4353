import unittest
from unittest.mock import patch, mock_open
import sys
sys.path.append('../')
from app import app
from routes import load_users, add_user, validate_email, validate_password, save_users, get_user_by_email
import json
from flask import Flask, session

# Remember to activate venv for tests to work

class TestUserAuth(unittest.TestCase):

    def setUp(self):
        # Configure Flask app for testing
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True
        # self.app = Flask(__name__)
        # self.app.secret_key = 'testkey'
        # self.client = self.app.test_client()

    # Mock the file operations so unit tests don't depend on actual files
    # @patch('routes.open', new_callable=mock_open, read_data='{"users": []}')
    @patch('routes.load_users', return_value={"users": [{"id": "1", "email": "testuser@example.com", "password": "testpassword", "admin": False}]})
    @patch('routes.save_users')
    def test_register_new_user(self, mock_save_users, mock_load_users):
        response = self.client.post('/api/register', json={
            "email": "newuser@example.com",
            "password": "testpassword"
        })
        self.assertEqual(response.status_code, 200)
        mock_save_users.assert_called()

    # @patch('routes.open', new_callable=mock_open, read_data='{"users": [{"id": "1", "email": "testuser@example.com", "password": "testpassword", "admin": false}]}')
    @patch('routes.load_users', return_value={"users": [{"id": "1", "email": "testuser@example.com", "password": "testpassword", "admin": False}]})
    @patch('routes.save_users')
    def test_register_existing_user(self, mock_save_users, mock_load_users):
        response = self.client.post('/api/register', json={
            "email": "testuser@example.com",
            "password": "newpassword"
        })
        # Response should indicate that user already exist
        self.assertEqual(response.status_code, 400)
        self.assertIn("An account with this email already exists", response.get_json()['msg'])
        mock_save_users.assert_not_called(); # Ensure save is not called since user already exists

    @patch('routes.load_users', return_value={"users": [{"id": "1", "email": "testuser@example.com", "password": "testpassword", "admin": False}]})
    def test_login_success(self, mock_load_users):
        response = self.client.post('/api/login', json={
            "email": "testuser@example.com",
            "password": "testpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login successful", response.get_json()['msg'])

    @patch('routes.load_users', return_value={"users": [{"id": "1", "email": "testuser@example.com", "password": "testpassword", "admin": False}]})
    def test_login_failure(self, mock_load_users):
        response = self.client.post('/api/login', json={
            "email": "testuser@example.com",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid email or password", response.get_json()['msg'])

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

    @patch('routes.os.path.exists', return_value=False)
    def test_load_users_file_not_exists(self, mock_exists):
        result = load_users()
        self.assertEqual(result, {"users": []}) # expecting an emtpy users list
        mock_exists.assert_called_once_with('dummy/users.json') # Ensure that path check was done

    @patch('routes.os.path.exists', return_value=True)
    @patch('routes.open', new_callable=mock_open, read_data='{"users": [{"id": "1", "email": "testuser@example.com", "password": "testpassword", "admin": false}]}')
    def test_load_users_file_exists(self, mock_open_file, mock_exists):
        result = load_users()
        expected_data = {"users": [{"id": "1", "email": "testuser@example.com", "password": "testpassword", "admin": False}]}
        self.assertEqual(result, expected_data)
        mock_exists.assert_called_once_with('dummy/users.json')
        mock_open_file.assert_called_once_with('dummy/users.json', 'r') # Ensure file was open in read mode

    # This test is better, probably delete the one above since it doesn't correctly mock loading
    @patch('routes.os.path.exists', return_value=True)
    @patch('routes.json.load')
    @patch('routes.open', new_callable=mock_open, read_data='{"users": [{"email": "testuser@example.com", "password": "password123"}]}')
    def test_load_users(self, mock_open_file, mock_json_load, mock_exists):
        mock_json_load.return_value = {"users": [{"email": "testuser@example.com", "password": "password123"}]}
        result = load_users()
        self.assertEqual(result, {"users": [{"email": "testuser@example.com", "password": "password123"}]})
        mock_exists.assert_called_once_with('dummy/users.json')
        mock_open_file.assert_called_once_with('dummy/users.json', 'r')
        mock_json_load.assert_called_once()

    @patch('routes.json.dump')
    @patch('routes.open', new_callable=mock_open)
    def test_save_users(self, mock_open_file, mock_json_dump):
        user_data = {"users": [{"id": "1", "email": "testuser@example.com", "password": "testpassword", "admin": False}]}
        save_users(user_data)
        mock_open_file.assert_called_once_with('dummy/users.json', 'w')
        mock_json_dump.assert_called_once_with(user_data, mock_open_file(), indent=4)

    @patch('routes.load_users', return_value={"users": [{"id": "1", "email": "testuser@example.com", "password": "testpassword", "admin": False}]})
    def test_get_user_by_email(self, mock_load_users):
        # Test correct email input
        result = get_user_by_email("testuser@example.com")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "1")
        
        # Test case sensitivity
        result = get_user_by_email("TESTUSER@EXAMPLE.COM")
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], "1")

        # Test no user found
        result = get_user_by_email("notfound@email.com")
        self.assertIsNone(result)

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

    @patch('routes.load_users', return_value = {"users": []})
    @patch('routes.save_users')
    def test_add_user(self, mock_save_users, mock_load_users):
        new_user = add_user("newuser@email.com", "password")
        self.assertEqual(new_user['id'], 1)
        self.assertEqual(new_user['email'], 'newuser@email.com')
        self.assertEqual(new_user['password'], 'password')
        self.assertFalse(new_user['admin'])

        saved_data = mock_save_users.call_args[0][0]
        self.assertEqual(len(saved_data['users']), 1) 

        new_user2 = add_user("newuser2@email.com", "password2")
        self.assertEqual(new_user2['id'], 2)
        self.assertEqual(new_user2['email'], 'newuser2@email.com')
        self.assertEqual(new_user2['password'], 'password2')
        self.assertFalse(new_user2['admin'])

        self.assertEqual(len(saved_data['users']), 2) 

        mock_save_users.assert_called()
        self.assertEqual(saved_data['users'][0], new_user)
        self.assertEqual(saved_data['users'][1], new_user2)




if __name__ == '__main__':
    unittest.main()

