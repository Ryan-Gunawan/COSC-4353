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
        # self.assertEqual(len(data), 1)

        event = data[0]
        self.assertEqual(event['name'], self.test_event_data['name'])
        self.assertEqual(event['location'], self.test_event_data['location'])
        self.assertEqual(event['date'], self.test_event_data['date'])

    def test_post_event(self):
        """Test creating a new event"""
        new_event_data = {
            'name': 'New Event',
            'description': 'A new event description',
            'location': 'New Location',
            'skills': 'Skill1, Skill2',
            'urgency': 'High',
            'date': '2024-12-30'
        }
        response = self.client.post('/api/newevent', data=json.dumps(new_event_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Event created successfully')

    def test_update_event(self):
        """Test updating an existing event"""
        updated_data = {
            'name': 'Updated Event',
            'description': 'Updated description',
            'location': 'Updated Location',
            'skills': 'Updated Skills',
            'urgency': 'Low',
            'date': '2024-12-31'
        }
        response = self.client.put(f'/api/eventlist/{self.test_event.id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Event updated successfully')

        # Fetch the updated event and verify changes
        updated_event = Event.query.get(self.test_event.id)
        self.assertEqual(updated_event.name, 'Updated Event')
        self.assertEqual(updated_event.description, 'Updated description')
        self.assertEqual(updated_event.location, 'Updated Location')
        self.assertEqual(updated_event.skills, 'Updated Skills')
        self.assertEqual(updated_event.urgency, 'Low')
        self.assertEqual(updated_event.date, '2024-12-31')

    def test_update_nonexistent_event(self):
        """Test updating a non-existent event"""
        updated_data = {
            'name': 'Nonexistent Event',
            'description': 'This event does not exist'
        }
        response = self.client.put('/api/eventlist/999', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Event not found')

    def test_delete_event(self):
        """Test deleting an existing event"""
        response = self.client.delete(f'/api/eventlist/{self.test_event.id}')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Event deleted successfully')

        # Verify that the event was deleted from the database
        deleted_event = Event.query.get(self.test_event.id)
        self.assertIsNone(deleted_event)

    def test_delete_nonexistent_event(self):
        """Test deleting a non-existent event"""
        response = self.client.delete('/api/eventlist/999')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'Event not found')


if __name__ == '__main__':
    unittest.main()
