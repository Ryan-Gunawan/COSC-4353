import unittest
import sys
sys.path.append('../')
from app import app
import json
import os
from flask import Flask, session
from unittest.mock import patch, MagicMock

class testEventList(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True

    @patch('app.Event')
    def test_get_events(self, mock_read_events):
        mock_event_instance = mock_read_events.query.get.return_value
        mock_event_instance.to_json.return_value = [{"assigned_users":[1,2],"date":"11-22-24","description":"We're doing some volunteering","id":1,"location":"Houston, TX","name":"Some event","skills":"leadership","urgency":"!"},
                                                   {"assigned_users":[1,2,3],"date":"2024-10-15 00:00:00","description":"Join us for a day of insightful talks and networking with industry leaders in technology.","id":2,"location":"San Francisco, CA","name":"Tech Conference 2024","skills":"[]","urgency":"MEDIUM"},
                                                   {"assigned_users":[1,2],"date":"2024-09-25 00:00:00","description":"A weekend filled with live music performances from top artists around the world.","id":3,"location":"Austin, TX","name":"Music Festival","skills":"[]","urgency":"MEDIUM"},
                                                   {"assigned_users":[1,2],"date":"2024-11-05 00:00:00","description":"Watch innovative startups pitch their ideas to investors and compete for prizes.","id":4,"location":"New York, NY","name":"Startup Pitch Night","skills":"[]","urgency":"MEDIUM"},
                                                   {"assigned_users":[1,2],"date":"2024-10-08 16:33:02","description":"$3.50 an hour","id":5,"location":"Houston","name":"Helping Teddy with his project","skills":"[\"Problem Solver\"]","urgency":"3"},
                                                   {"assigned_users":[1,2],"date":"2024-10-19 00:00:00","description":"Updated Description","id":6,"location":"Updated Location","name":"Updated Event Name","skills":"[\"Skill1\", \"Skill2\"]","urgency":"High"}]

        response = self.client.get('/api/eventlist')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), mock_event_instance.to_json())

    @patch('app.db.session.commit')
    @patch('app.Event')
    def test_update_event_success(self, mock_get, mock_commit):
        # Create a mock event object
        mock_event = MagicMock()
        mock_event.id = 1
        mock_event.name = "Some event"
        mock_event.description = "We're doing some volunteering"
        mock_event.location = "Houston, TX"
        mock_event.date = "11-22-24"
        mock_event.skills = "leadership"
        mock_event.urgency = "!"
        mock_event.assigned_users = [1, 2]

        # Prepare the data for the update
        updated_data = {
            "location": "Dallas, TX"
        }

        # Send a PUT request to update the event
        response = self.client.put(f'/api/eventlist/{mock_event.id}', data=json.dumps(updated_data), content_type='application/json')

        # Simulate change of database
        mock_event.location = updated_data['location']

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['msg'], 'Event updated successfully')
        self.assertEqual(mock_event.location, "Dallas, TX")

        # Check that commit was called once
        mock_commit.assert_called_once()

    @patch('app.db.session.commit')
    @patch('app.db.session.add')
    @patch('models.Event')
    def test_post_event(self, mock_event, mock_add, mock_commit):
        # Prepare the data to be sent in the POST request
        event_data = {
            "name": "Mock event",
            "description": "",
            "location": "U.S.",
            "skills": [],
            "urgency": "medium",
            "date": ""
        }

        # Create a mock Event instance
        mock_event_instance = MagicMock()
        mock_event.return_value = mock_event_instance

        # Send a POST request to the /api/newevent endpoint
        response = self.client.post('/api/newevent', data=json.dumps(event_data), content_type='application/json')

        mock_event.assert_called_once_with(
            name="Mock event",
            description="",
            location="U.S.",
            skills=[],
            urgency="medium",
            date=""
        )

        # Assert the response
        mock_add.assert_called_once_with(mock_event_instance)
        mock_commit.assert_called_once()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['msg'], 'Event created successfully')
        
if __name__ == '__main__':
    unittest.main()
