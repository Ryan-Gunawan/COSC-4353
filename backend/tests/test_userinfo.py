import unittest
from app import app
import json
import os
import sys
sys.path.append('../')
from flask import Flask, session
# from routes import get_userinfo, update_userinfo
from unittest.mock import patch, MagicMock
from models import User

class TestUserInfo(unittest.TestCase):
    def setUp(self):

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True
        self.app = app
        self.app_context = self.app.app_context()
        
    @patch('app.User')
    def test_get_userinfo(self, mock_user):
        # Mocking session
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1

            # Mock user retrieval and .to_json() method
            mock_user_instance = mock_user.query.get.return_value
            mock_user_instance.to_json.return_value = {'address1': '123 Banana St.', 'address2': '', 'admin': False, 'availability': ['2024-10-22'], 'city': 'Houston', 'email': 'email@gmail.com', 'fullname': 'Bob Brown', 'history': ['Tech Conference 2024', 'Music Festival', 'Startup Pitch Night', 'Helping Teddy with his project', 'Updated Event Name', 'Some event'], 'id': 1, 'preference': '', 'skills': ['communication', 'creativity'], 'state': 'TX', 'zipcode': '12345'}

            response = client.get("/api/userprofile")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, mock_user_instance.to_json())

    @patch('app.db.session.commit')
    @patch('app.User')
    def test_update_userinfo(self, mock_get, mock_commit):
        # Create a mock user object
        mock_user = MagicMock()
        mock_user.fullname = 'Musk'
        mock_user.address1 = '123 Maple Syrup'
        mock_user.address2 = ''
        mock_user.city = 'Houston'
        mock_user.state = 'TX'
        mock_user.zipcode = '12345'
        mock_user.skills = ["communication", "creativity"]
        mock_user.preference = ''
        mock_user.availability = ["2024-10-22"]

        updated_data = {
            "fullname": "Musk",
            "address1": "99 Maple Syrup",
            "address2": "",
            "city": "Houston",
            "state": "TX",
            "zipcode": "99999",
            "skills": ["communication", "creativity"],
            "preference": "",
            "availability": []
        }

        # Send a PUT request to update the user profile
        response = self.client.put('/api/userprofile/1', data=json.dumps(updated_data), content_type='application/json')

        # Simulate change of database
        mock_user.address1 = updated_data['address1']
        mock_user.zipcode = updated_data['zipcode']
        mock_user.availability = updated_data['availability']

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['msg'], 'User info updated successfully')
        self.assertEqual(mock_user.address1, '99 Maple Syrup')
        self.assertEqual(mock_user.zipcode, '99999')
        self.assertEqual(mock_user.availability, [])

        # Check that commit was called once
        mock_commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()