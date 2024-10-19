import unittest
from app import app
import json
import os
import sys
sys.path.append('../')
from flask import Flask, session
from unittest.mock import patch

class testEventList(unittest.TestCase):
    def setUp(self):

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True

    @patch('os.path.exists')  # Mock data access
    def test_get_event_list(self, mock_get_eventlist):
        with self.client as client:
            with client.session_transaction() as sess:
                sess['id'] = "1" #Mock session
            response = client.get('/api/eventlist')
            data = json.loads(response.data)

            expected_data = [
    {
        "id": 1,
        "name": "Tech Conference 2024",
        "date": "2024-10-15",
        "location": "San Francisco, CA",
        "description": "Join us for a day of insightful talks and networking with industry leaders in technology.",
        "assignedUsers": []
    },
    {
        "id": 2,
        "name": "Music Festival",
        "date": "2024-09-25",
        "location": "Austin, TX",
        "description": "A weekend filled with live music performances from top artists around the world.",
        "assignedUsers": []
    },
    {
        "id": 3,
        "name": "Startup Pitch Night",
        "date": "2024-11-05",
        "location": "New York, NY",
        "description": "Watch innovative startups pitch their ideas to investors and compete for prizes.",
        "assignedUsers": []
    },
    {
        "id": 4,
        "name": "Helping Teddy with his project",
        "description": "$3.50 an hour",
        "location": "Houston",
        "skills": [
            "Problem Solver"
        ],
        "urgency": "3",
        "date": "2024-10-08T16:33:02",
        "assignedUsers": []
    },
    {
        "id": 5,
        "name": "Updated Event Name",
        "description": "Updated Description",
        "location": "Updated Location",
        "skills": [
            "Skill1",
            "Skill2"
        ],
        "urgency": "High",
        "date": "2024-10-19",
        "assignedUsers": ["1"]
    }
]

            self.assertEqual(data, expected_data)
