import unittest
from unittest.mock import patch, MagicMock
from app import app
from flask import json

class EventMatcherAPITestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test for GET /api/events
    @patch('app.db.session.query')
    def test_get_events(self, mock_query):
        """Test fetching the event list from the /api/events route."""
        # Mock the database response
        mock_query.return_value.all.return_value = [
            MagicMock(id=1, name="Event 1", date="2024-11-01", location="Location 1", description="Description 1"),
            MagicMock(id=2, name="Event 2", date="2024-11-02", location="Location 2", description="Description 2"),
        ]
        
        response = self.app.get('/api/events')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        # Parse the response data
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], "Event 1")
        self.assertEqual(data[1]['location'], "Location 2")

    # Test for GET /api/userslist
    @patch('app.db.session.query')
    def test_get_users_list(self, mock_query):
        """Test fetching the user list from the /api/userslist route."""
        # Mock the database response
        mock_query.return_value.all.return_value = [
            MagicMock(id=1, email="user1@example.com", volunteer=[]),
            MagicMock(id=2, email="user2@example.com", volunteer=[]),
        ]
        
        response = self.app.get('/api/userslist')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        
        # Parse the response data
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['email'], "user1@example.com")

    # Test for PUT /api/match_user (successful match)
    @patch('app.db.session.commit')
    @patch('app.db.session.query')
    def test_match_user_successful(self, mock_query, mock_commit):
        """Test matching a user to an event successfully through /api/match_user."""
        # Mock user and event in the database
        mock_user = MagicMock(id=1, volunteer=[1])
        mock_event = MagicMock(id=3)
        mock_query.return_value.get.side_effect = lambda x: mock_user if x == 1 else mock_event

        response = self.app.put('/api/match_user', json={"user_id": 1, "event_id": 3})
        self.assertEqual(response.status_code, 200)
        
        # Check the response message and updated volunteer list
        data = json.loads(response.data)
        self.assertEqual(data['msg'], "Event added to volunteer list")
        mock_commit.assert_called_once()

    # Test for PUT /api/match_user (user already matched to event)
    @patch('app.db.session.commit')
    @patch('app.db.session.query')
    def test_user_already_matched(self, mock_query, mock_commit):
        """Test trying to match a user who is already matched to an event."""
        # Mock user with event already in volunteer list
        mock_user = MagicMock(id=1, volunteer=[3])
        mock_event = MagicMock(id=3)
        mock_query.return_value.get.side_effect = lambda x: mock_user if x == 1 else mock_event

        response = self.app.put('/api/match_user', json={"user_id": 1, "event_id": 3})
        self.assertEqual(response.status_code, 200)

        # Check the response message indicating the user is already matched
        data = json.loads(response.data)
        self.assertEqual(data['msg'], "Event already in volunteer list")
        mock_commit.assert_not_called()

    # Test for PUT /api/match_user (user not found)
    @patch('app.db.session.query')
    def test_user_not_found(self, mock_query):
        """Test trying to match a user who doesn't exist."""
        # Mock that user is not found
        mock_query.return_value.get.side_effect = lambda x: None if x == 1 else MagicMock(id=3)

        response = self.app.put('/api/match_user', json={"user_id": 99, "event_id": 3})
        self.assertEqual(response.status_code, 404)

        # Check the response message for user not found
        data = json.loads(response.data)
        self.assertEqual(data['msg'], "User not found")

    # Test for PUT /api/match_user (event not found)
    @patch('app.db.session.query')
    def test_event_not_found(self, mock_query):
        """Test trying to match an event that doesn't exist."""
        # Mock that event is not found
        mock_user = MagicMock(id=1, volunteer=[])
        mock_query.return_value.get.side_effect = lambda x: mock_user if x == 1 else None

        response = self.app.put('/api/match_user', json={"user_id": 1, "event_id": 99})
        self.assertEqual(response.status_code, 404)

        # Check the response message for event not found
        data = json.loads(response.data)
        self.assertEqual(data['msg'], "Event not found")

if __name__ == '__main__':
    unittest.main()
