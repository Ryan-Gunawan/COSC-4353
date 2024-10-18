import unittest
from unittest.mock import patch, mock_open
import sys
sys.path.append('../')
from app import app
from routes import read_users_from_file, read_events_from_file
import json
from flask import Flask, session

class TestEventMatching(unittest.TestCase):

    def setUp(self):
        # Configure Flask app for testing
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey'  # for session testing
        self.client = app.test_client()  # create a test client

    @patch('routes.read_users_from_file', return_value={
        "users": [
            {
                "id": "1",
                "email": "elon@example.com",
                "fullname": "Elon Musk",
                "skills": ["Creativity", "Leadership"],
                "availability": ["2024-10-10"],
                "volunteer": []
            }
        ]
    })
    @patch('routes.read_events_from_file', return_value=[
        {
            "id": 1,
            "name": "Music Festival",
            "date": "2024-10-15",
            "location": "Austin, TX",
            "description": "A weekend filled with live music performances.",
            "requiredSkills": ["Leadership"],
            "assignedUsers": []
        }
    ])
    def test_user_can_be_matched_to_event(self, mock_load_events, mock_load_users):
        # Match user to event
        user_id = "1"
        event_id = 1
        response = self.client.post(f'/api/match/{user_id}/{event_id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn("User matched successfully", response.get_json()['msg'])

    @patch('routes.read_users_from_file', return_value={
        "users": [
            {
                "id": "1",
                "email": "elon@example.com",
                "fullname": "Elon Musk",
                "skills": ["Creativity", "Leadership"],
                "availability": ["2024-10-10"],
                "volunteer": [1]  # Already matched
            }
        ]
    })
    @patch('routes.read_events_from_file', return_value=[
        {
            "id": 1,
            "name": "Music Festival",
            "date": "2024-10-15",
            "location": "Austin, TX",
            "description": "A weekend filled with live music performances.",
            "requiredSkills": ["Leadership"],
            "assignedUsers": []
        }
    ])
    def test_user_already_matched_to_event(self, mock_load_events, mock_load_users):
        # Attempt to match user who is already matched
        user_id = "1"
        event_id = 1
        response = self.client.post(f'/api/match/{user_id}/{event_id}')

        self.assertEqual(response.status_code, 400)
        self.assertIn("Volunteer has already been matched to this event", response.get_json()['msg'])

    @patch('routes.read_users_from_file', return_value={
        "users": [
            {
                "id": "1",
                "email": "elon@example.com",
                "fullname": "Elon Musk",
                "skills": ["Creativity", "Leadership"],
                "availability": ["2024-10-10"],
                "volunteer": []
            }
        ]
    })
    @patch('routes.read_events_from_file', return_value=[
        {
            "id": 1,
            "name": "Music Festival",
            "date": "2024-10-15",
            "location": "Austin, TX",
            "description": "A weekend filled with live music performances.",
            "requiredSkills": ["Teamwork"],  # User doesn't have this skill
            "assignedUsers": []
        }
    ])
    def test_user_cannot_be_matched_due_to_skills(self, mock_load_events, mock_load_users):
        # Attempt to match user without required skills
        user_id = "1"
        event_id = 1
        response = self.client.post(f'/api/match/{user_id}/{event_id}')

        self.assertEqual(response.status_code, 400)
        self.assertIn("User does not meet the required skills", response.get_json()['msg'])

    @patch('routes.read_users_from_file', return_value={
        "users": [
            {
                "id": "1",
                "email": "elon@example.com",
                "fullname": "Elon Musk",
                "skills": ["Creativity", "Leadership"],
                "availability": [],  # No availability
                "volunteer": []
            }
        ]
    })
    @patch('routes.read_events_from_file', return_value=[
        {
            "id": 1,
            "name": "Music Festival",
            "date": "2024-10-15",
            "location": "Austin, TX",
            "description": "A weekend filled with live music performances.",
            "requiredSkills": ["Leadership"],
            "assignedUsers": []
        }
    ])
    def test_user_with_no_availability_can_be_matched(self, mock_load_events, mock_load_users):
        # Match user with no defined availability
        user_id = "1"
        event_id = 1
        response = self.client.post(f'/api/match/{user_id}/{event_id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn("User matched successfully", response.get_json()['msg'])

if __name__ == '__main__':
    unittest.main()
