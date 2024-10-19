import unittest
import sys
sys.path.append('../')
from app import app
import json
import os
from flask import Flask, session
from unittest.mock import patch

class testEventList(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True

    @patch('routes.read_events_from_file')
    def test_get_events(self, mock_read_events):
        mock_read_events.return_value = [
            {
                "id": 1,
                "name": "Tech Conference 2024",
                "date": "2024-10-15",
                "location": "San Francisco, CA",
                "description": "Join us for a day of insightful talks and networking with industry leaders in technology.",
                "assignedUsers": []
            }
        ]

        response = self.client.get('/api/eventlist')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {
                "id": 1,
                "name": "Tech Conference 2024",
                "date": "2024-10-15",
                "location": "San Francisco, CA",
                "description": "Join us for a day of insightful talks and networking with industry leaders in technology.",
                "assignedUsers": []
            }
        ])
        mock_read_events.assert_called_once()


    @patch('routes.read_events_from_file')
    @patch('routes.add_events_to_file')
    def test_update_event_success(self, mock_add_events, mock_read_events):
        mock_read_events.return_value = [
            {
                "id": 1,
                "name": "Tech Conference 2024",
                "date": "2024-10-15",
                "location": "San Francisco, CA",
                "description": "Event description",
                "assignedUsers": []
            }
        ]

        updated_data = {"name": "Updated Event Name"}

        # Act: Send PUT request to update event 1
        response = self.client.put('/api/eventlist/1', json=updated_data)

        # Assert: Ensure correct status code and that the event was updated
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"msg": "Event updated successfully"})
        expected_events = [
            {
                "id": 1,
                "name": "Updated Event Name", # Expected to have an updated name
                "date": "2024-10-15",
                "location": "San Francisco, CA",
                "description": "Event description",
                "assignedUsers": []
            }
        ]

        mock_add_events.assert_called_once_with(expected_events)


if __name__ == '__main__':
    unittest.main()
