import unittest
import sys
sys.path.append('../')
from app import app, db
import json
import os
from flask import Flask, session
# from unittest.mock import patch, MagicMock
from models import User, Event

class TestUserInfo(unittest.TestCase):
    def setUp(self):

        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True
        self.app_context = app.app_context()
        self.app_context.push()

        db.create_all()

        # Create test user
        self.test_user = User(
            id = '1',
            email = 'email@gmial.com',
            password = 'password',
            fullname = 'Full Name',
            address1 = '50 Harvey Drive',
            city = 'Campbell',
            state = 'CA',
            zipcode = '95008'
        )
        db.session.add(self.test_user)

        # Create test event
        self.test_event = Event(
            name='Test Event',
            location='Test Location',
            date='2024-12-25'
        )
        self.test_event.assigned_users.append(self.test_user)
        db.session.add(self.test_event)
        db.session.commit()

         # Store test data for comparison
        self.test_user_data = {
            'id': '1',
            'email': 'email@gmial.com',
            'password': 'password',
            'fullname':'Full Name',
            'address1': '50 Harvey Drive',
            'city': 'Campbell',
            'state': 'CA',
            'zipcode': '95008'
        }

        self.test_event_data = {
            'name': 'Test Event',
            'location': 'Test Location',
            'date': '2024-12-25'
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_history(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.test_user.id

        response = self.client.get('api/volunteerhistory')
        self.assertEqual(response.status_code, 200)
        
        # Load JSON data from the response
        data = json.loads(response.data)

        # Expected output from the get_history function
        self.assertEqual(data[0]['name'], self.test_event_data['name'])
        self.assertEqual(data[0]['location'], self.test_event_data['location'])
        self.assertEqual(data[0]['date'], self.test_event_data['date'])
    
if __name__ == '__main__':
    unittest.main()
