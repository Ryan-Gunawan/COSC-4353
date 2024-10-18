import unittest
from app import app
import json
import os
import sys
sys.path.append('../')
from flask import Flask, session
from routes import get_userinfo, update_userinfo
from unittest.mock import patch, mock_open

class TestUserInfo(unittest.TestCase):
    def setUp(self):

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True

    def tearDown(self):
        pass

    # Mock testing
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'users': [{'id': "1",'email': "email@gmail.com",'password': "password",
            'admin': False,'fullname': "Elon Musk",'address1': "123 Maple Street",'address2': "",'city': "Austin",'state': "TX",'zipcode': "78701",
            'skills': ["children","creativity","responsibility"],'preference': "",'availability': ["2025-10-10","2025-10-23","2025-10-14"],'volunteer': [1, 2, 4]}]}))
    @patch('os.path.exists', return_value=True)
    def test_get_userinfo(self, mock_exists, mock_open):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_id'] = "1"  # Mock the session

            # Send GET request to the /api/userprofile route
            response = client.get('/api/userprofile')
            data = json.loads(response.data)

            # Check if the file was opened for reading and writing
            mock_open.assert_called_with('dummy/users.json', 'r')
            
            # Assert the status code
            self.assertEqual(response.status_code, 200)
            expected_data = [{"id": "1",
                    "email": "email@gmail.com",
                    "password": "password",
                    "admin": False,
                    "fullname": "Elon Musk",
                    "address1": "123 Maple Street",
                    "address2": "",
                    "city": "Austin",
                    "state": "TX",
                    "zipcode": "78701",
                    "skills": ["children", "creativity", "responsibility"],
                    "preference": "",
                    "availability": ["2025-10-10", "2025-10-23", "2025-10-14"],
                    "volunteer": [1, 2, 4]}]
            self.assertEqual(data, expected_data)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'users': [{'id': "1",'email': "email@gmail.com",'password': "password",
            'admin': False,'fullname': "Elon Musk",'address1': "123 Maple Street",'address2': "",'city': "Austin",'state': "TX",'zipcode': "78701",
            'skills': ["children","creativity","responsibility"],'preference': "",'availability': ["2025-10-10","2025-10-23","2025-10-14"],'volunteer': [1, 2, 4]}]}))
    @patch('os.path.exists', return_value=True)
    @patch('json.dump')
    def test_update_userinfo(self, mock_json_dump, mock_exists, mock_open): 

        with self.client as client:
        # Define the updated data
            update_data = {
                "fullname": "Musk",
                "address1": "123 Maple Syrup",
            }

            # Mocking the writing data
            written_data = {}
            def json_dump_side_effect(data, file, indent):
                nonlocal written_data
                written_data = data  # Store the data passed to json.dump
            mock_json_dump.side_effect = json_dump_side_effect
            
            response = client.put('/api/userprofile/1', json=update_data)
            
            # Check if the file was opened for reading and writing
            mock_open.assert_any_call('dummy/users.json', 'r')
            mock_open.assert_any_call('dummy/users.json', 'w')
            updated_users = written_data['users']

            # Assert 
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), {"msg": "User info updated successfully"})
            self.assertEqual(updated_users[0]['fullname'], "Musk")
            self.assertEqual(updated_users[0]['address1'], "123 Maple Syrup")

if __name__ == '__main__':
    unittest.main()