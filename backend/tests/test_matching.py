import unittest
from unittest.mock import patch, MagicMock
import json
import sys
sys.path.append('../')
from app import app, db  # Import the Flask app and database

class EventMatcherAPITestCase(unittest.TestCase):
    
    def setUp(self):
        # Create a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    # Test for GET /api/users
    @patch('app.db.session.query')
    def test_get_users_list(self, mock_query):
        """Test fetching the user list from the /api/users route."""
        # Mocked user data returned from database query
        mock_users = [
            MagicMock(id=1, email="user1@example.com", fullname="User One", volunteer=[]),
            MagicMock(id=2, email="user2@example.com", fullname="User Two", volunteer=[])
        ]
        # Configure query to return mock users
        mock_query.return_value.all.return_value = mock_users

        # Send GET request
        response = self.app.get('/api/users')
        
        # Check response status and content type
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

        # Parse the JSON response and verify the data structure
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["email"], "user1@example.com")

    # Test for PUT /api/match_user for successful matching
    @patch('app.db.session.commit')
    @patch('app.db.session.query')
    def test_match_user_success(self, mock_query, mock_commit):
        """Test matching a user to an event with /api/match_user route."""
        # Mock user with an empty volunteer list
        mock_user = MagicMock(id=1, volunteer=[])
        
        # Configure the query mock to return the mock user and a valid event
        mock_query.side_effect = lambda model: [mock_user] if model.__name__ == 'User' else [MagicMock(id=3)]
        
        # Send PUT request
        response = self.app.put('/api/match_user', json={"user_id": 1, "event_id": 3})
        
        # Verify successful match response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Event added to volunteer list')
        self.assertIn(3, mock_user.volunteer)

    # Test for PUT /api/match_user when user is already matched to the event
    @patch('app.db.session.commit')
    @patch('app.db.session.query')
    def test_user_already_matched(self, mock_query, mock_commit):
        """Test matching a user who is already matched to an event."""
        # Mock user with an existing event in the volunteer list
        mock_user = MagicMock(id=1, volunteer=[3])
        
        # Configure query mock to return the mock user
        mock_query.return_value.filter_by.return_value.first.return_value = mock_user
        
        # Send PUT request
        response = self.app.put('/api/match_user', json={"user_id": 1, "event_id": 3})
        
        # Verify already matched response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Event already in volunteer list')

    # Test for PUT /api/match_user when user is not found
    @patch('app.db.session.query')
    def test_user_not_found(self, mock_query):
        """Test trying to match a user who doesn't exist."""
        # Configure query to return None for a non-existent user
        mock_query.return_value.filter_by.return_value.first.return_value = None
        
        # Send PUT request
        response = self.app.put('/api/match_user', json={"user_id": 99, "event_id": 3})
        
        # Verify user not found response
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'User not found')

    # Test for PUT /api/match_user when event is not found
    @patch('app.db.session.query')
    def test_event_not_found(self, mock_query):
        """Test trying to match a user to a non-existent event."""
        # Mock a valid user but configure event query to return None
        mock_user = MagicMock(id=1, volunteer=[])
        mock_query.side_effect = lambda model: [mock_user] if model.__name__ == 'User' else None
        
        # Send PUT request
        response = self.app.put('/api/match_user', json={"user_id": 1, "event_id": 99})
        
        # Verify event not found response
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Event not found')

if __name__ == '__main__':
    unittest.main()
