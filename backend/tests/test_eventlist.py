import unittest
import sys
sys.path.append('../')
from app import app, db
from models import User, Event
import json
import os
from flask import Flask, session

class testEventList(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

        # Create all tables
        db.create_all()

        # Create test event
        self.test_event = Event(
            name='Test Event',
            location='Test Location',
            date='2024-12-25'
        )
        db.session.add(self.test_event)
        db.session.commit()

        # Store test event data for comparison
        self.test_event_data = {
            'name': 'Test Event',
            'location': 'Test Location',
            'date': '2024-12-25'
        }

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_events(self):
        """Test getting all events"""
        response = self.client.get('/api/eventlist')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)

        event = data[0]
        self.assertEqual(event['name'], self.test_event_data['name'])
        self.assertEqual(event['location'], self.test_event_data['location'])
        self.assertEqual(event['date'], self.test_event_data['date'])

        
if __name__ == '__main__':
    unittest.main()
