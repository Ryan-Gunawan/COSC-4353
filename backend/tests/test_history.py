import unittest
from app import app
import json
import os
import sys
sys.path.append('../')
from flask import Flask, session
from unittest.mock import patch

class TestUserInfo(unittest.TestCase):
    def setUp(self):

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True

    @patch('os.path.exists')  # Mock data access
    def test_get_volunteer_history(self, mock_get_history):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_id'] = "1" #Mock session
            response = client.get('/api/volunteerhistory')
            data = json.loads(response.data)

            # Expected volunteer history data
            expected_data = [{"assignedUsers":[],"date":"2024-10-15","description":"Join us for a day of insightful talks and networking with industry leaders in technology.","id":1,"location":"San Francisco, CA","name":"Tech Conference 2024"},
                            {"assignedUsers":[],"date":"2024-09-25","description":"A weekend filled with live music performances from top artists around the world.","id":2,"location":"Austin, TX","name":"Music Festival"},
                            {"assignedUsers":[],"date":"2024-10-08T16:33:02","description":"$3.50 an hour","id":4,"location":"Houston","name":"Helping Teddy with his project","skills":["Problem Solver"],"urgency":"3"}]

            # Assert that the returned data matches the expected event data
            self.assertEqual(data, expected_data)