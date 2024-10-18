import unittest
from unittest.mock import patch, mock_open
import sys
sys.path.append('../')
from app import app
from routes import app, read_users_from_file, match_user  # Importing functions from your routes module
import json
from flask import Flask, session


class UserAPITestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test for GET /api/usersList
    @patch('routes.read_users_from_file', return_value={"users": [{"id": "1", "email": "testuser@example.com", "password": "testpassword"}]})
    def test_get_users_list(self, mock_read_users_from_file):
        """Test fetching the user list from the /api/usersList route."""
        response = self.app.get('/api/usersList')
        self.assertEqual(response.status_code, 200)

        # Check if the response is JSON
        self.assertEqual(response.content_type, 'application/json')

        # Verify the mocked function is called
        mock_read_users_from_file.assert_called_once()

        # Parse the response data and assert the structure
        data = json.loads(response.data)
        self.assertIn('users', data)
        self.assertEqual(data['users'][0]['id'], "1")
        self.assertEqual(data['users'][0]['email'], "testuser@example.com")

    # Test for POST /api/match_user
    @patch('routes.open', new_callable=mock_open, read_data='{"users": [{"id": "1", "email": "testuser@example.com", "volunteer": [2]}]}')
    def test_match_user(self, mock_file):
        """Test matching a user to an event from the /api/match_user route."""
        response = self.app.post('/api/match_user', json={
            "user_id": "1",
            "event_id": 3
        })

        # Check the status code of the response
        self.assertEqual(response.status_code, 200)

        # Verify that the data was written to the file
        mock_file().write.assert_called()

        # Check the response message
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User matched successfully!')

    @patch('routes.open', new_callable=mock_open, read_data='{"users": [{"id": "1", "email": "testuser@example.com", "volunteer": [1, 2, 3]}]}')
    def test_user_already_matched(self, mock_file):
        """Test trying to match a user who is already matched to an event."""
        response = self.app.post('/api/match_user', json={
            "user_id": "1",
            "event_id": 3
        })

        # Check if the response status is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Check if the correct message is returned
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Volunteer has already been matched to this event.')

    @patch('routes.open', new_callable=mock_open, read_data='{"users": [{"id": "1", "email": "testuser@example.com", "volunteer": []}]}')
    def test_user_not_found(self, mock_file):
        """Test trying to match a user who doesn't exist."""
        response = self.app.post('/api/match_user', json={
            "user_id": "99",
            "event_id": 3
        })

        # Check if the response status is 404 (Not Found)
        self.assertEqual(response.status_code, 404)

        # Check if the correct message is returned
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'User not found.')

if __name__ == '__main__':
    unittest.main()
