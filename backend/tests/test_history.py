import unittest
import sys
sys.path.append('../')
from app import app, db
import json
import os
from flask import Flask, session
from unittest.mock import patch, MagicMock

# Run test in backend for this to work and avoid open file error

class TestUserInfo(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True

    @patch('app.User')
    def test_get_history(self, mock_user):
        #  Mock user_id session
        with self.client as client:
            with client.session_transaction() as sess:
                sess['user_id'] = 1

            # Mock User.query.get() to return a user
            mock_user_instance = mock_user.query.get.return_value
            
            # Get real and expected data
            response = client.get("/api/volunteerhistory")
            expected = [{"assigned_users":[1,2,3],"date":"2024-10-15 00:00:00","description":"Join us for a day of insightful talks and networking with industry leaders in technology.","id":2,"location":"San Francisco, CA","name":"Tech Conference 2024","skills":"[]","urgency":"MEDIUM"},{"assigned_users":[1,2],"date":"2024-09-25 00:00:00","description":"A weekend filled with live music performances from top artists around the world.","id":3,"location":"Austin, TX","name":"Music Festival","skills":"[]","urgency":"MEDIUM"},{"assigned_users":[1,2],"date":"2024-11-05 00:00:00","description":"Watch innovative startups pitch their ideas to investors and compete for prizes.","id":4,"location":"New York, NY","name":"Startup Pitch Night","skills":"[]","urgency":"MEDIUM"},{"assigned_users":[1,2],"date":"2024-10-08 16:33:02","description":"$3.50 an hour","id":5,"location":"Houston","name":"Helping Teddy with his project","skills":"[\"Problem Solver\"]","urgency":"3"},{"assigned_users":[1,2],"date":"2024-10-19 00:00:00","description":"Updated Description","id":6,"location":"Updated Location","name":"Updated Event Name","skills":"[\"Skill1\", \"Skill2\"]","urgency":"High"},{"assigned_users":[1,2],"date":"11-22-24","description":"We're doing some volunteering","id":1,"location":"Houston, TX","name":"Some event","skills":"leadership","urgency":"!"}]

            # Assert status code and response data
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, expected)

if __name__ == '__main__':
    unittest.main()
