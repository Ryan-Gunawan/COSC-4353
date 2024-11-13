import unittest
from unittest.mock import patch, MagicMock
import json
import sys
sys.path.append('../')
from app import app, db
from models import User, Event

class EventMatcherAPITestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'testkey'
        self.client = app.test_client()
        self.client.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

        # Create all tables
        db.create_all()

        # Create test user
        self.test_user = User(
            email='email@gmail.com',
            password='password',
            fullname='Full Name',
            address1='50 Harvey Drive',
            city='Campbell',
            state='CA',
            zipcode='95008'
        )
        db.session.add(self.test_user)

        # Create test event
        self.test_event = Event(
            name='Test Event',
            location='Test Location',
            date='2024-12-25'
        )
        db.session.add(self.test_event)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_users_list(self):
        """Test fetching the user list from the /api/users route."""
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['email'], 'email@gmail.com')

    def test_match_user_success(self):
        """Test matching a user to an event successfully."""
        response = self.client.put('/api/match_user', json={
            'user_id': 1,
            'event_id': 1
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Event added to volunteer list and notification sent')

    def test_match_user_duplicate(self):
        """Test matching a user to an event that is already matched."""
        # First match
        self.client.put('/api/match_user', json={
            'user_id': 1,
            'event_id': 1
        })
        # Try matching again
        response = self.client.put('/api/match_user', json={
            'user_id': 1,
            'event_id': 1
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Event already in volunteer list')

    def test_match_user_not_found(self):
        """Test matching a non-existent user to an event."""
        response = self.client.put('/api/match_user', json={
            'user_id': 999,
            'event_id': 1
        })
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'User not found')

    def test_match_event_not_found(self):
        """Test matching a user to a non-existent event."""
        response = self.client.put('/api/match_user', json={
            'user_id': 1,
            'event_id': 999
        })
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Event not found')

if __name__ == '__main__':
    unittest.main()
