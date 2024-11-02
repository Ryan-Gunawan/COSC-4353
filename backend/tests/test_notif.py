import unittest
from unittest.mock import patch, mock_open
import sys
sys.path.append('../')
from app import app, db
import json
from flask import Flask, session
from routes import get_notifications, delete_notification, send_reminder_notifications, send_event_update_notifications
from routes import scheduler
from models import User, Event, Notification
from datetime import datetime, timedelta, date

class TestNotifications(unittest.TestCase):
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
            email='test@example.com',
            password='TestPass123!',
            admin=False
        )
        self.test_user.set_password('TestPass123!')
        db.session.add(self.test_user)

        # Create test notification
        self.test_notification = Notification(
            user_id=1,
            title="Test Notification",
            date=date.today().strftime("%Y-%m-%d"),
            message="Test message",
            notif_type="test"
        )
        db.session.add(self.test_notification)
        db.session.commit()

    def tearDown(self):
        scheduler.remove_all_jobs()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def login_test_user(self):
        """Helper method to login test user"""
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.test_user.id

    def test_get_notifications(self):
        """Test getting user notifications"""
        self.login_test_user()
        
        response = self.client.get('/api/notifications')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Test Notification')

    # def test_get_notifications_unauthorized(self):
    #     """Test getting notifications without login"""
    #     response = self.client.get('/api/notifications')
    #     self.assertEqual(response.status_code, 401)

    def test_delete_notification(self):
        """Test deleting a notification"""
        self.login_test_user()
        
        response = self.client.delete('/api/notifications',
            json={'notification_id': self.test_notification.id}
        )
        self.assertEqual(response.status_code, 204)
        
        # Verify notification was deleted
        notification = Notification.query.get(self.test_notification.id)
        self.assertIsNone(notification)

    def test_delete_notification_unauthorized(self):
        """Test deleting notification without login"""
        response = self.client.delete('/api/notifications',
            json={'notification_id': self.test_notification.id}
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_notification_missing_id(self):
        """Test deleting notification without providing ID"""
        self.login_test_user()
        response = self.client.delete('/api/notifications',
            json={}
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_nonexistent_notification(self):
        """Test deleting a notification that doesn't exist"""
        self.login_test_user()
        response = self.client.delete('/api/notifications',
            json={'notification_id': 9999}
        )
        self.assertEqual(response.status_code, 404)

    def test_send_assignment_notification(self):
        """Test sending assignment notification"""
        test_data = {
            'userId': self.test_user.id,
            'eventName': 'Test Event',
            'eventDate': '2024-12-25'
        }
        
        response = self.client.post('/api/send-assignment-notification',
            json=test_data
        )
        self.assertEqual(response.status_code, 200)
        
        # Verify notification was created
        notification = Notification.query.filter_by(
            user_id=self.test_user.id,
            notif_type='assignment'
        ).first()
        self.assertIsNotNone(notification)
        self.assertIn('Test Event', notification.message)

    def test_send_assignment_notification_missing_fields(self):
        """Test sending assignment notification with missing fields"""
        test_data = {
            'userId': self.test_user.id,
            'eventName': 'Test Event'
            # Missing eventDate
        }
        
        response = self.client.post('/api/send-assignment-notification',
            json=test_data
        )
        self.assertEqual(response.status_code, 400)

    def test_send_reminder_notifications(self):
        """Test sending reminder notifications for upcoming events"""
        # Create test event for tomorrow
        tomorrow = date.today() + timedelta(days=1)
        test_event = Event(
            name='Test Event',
            description='Test description',
            date=tomorrow.strftime('%Y-%m-%d'),
            location='Somewhere'
        )

        test_event.assigned_users.append(self.test_user)
        db.session.add(test_event)
        db.session.commit()

        # Run the reminder notification function
        send_reminder_notifications()

        # Verify reminder notification was created
        notification = Notification.query.filter_by(
            user_id=self.test_user.id,
            notif_type='reminder'
        ).first()
        self.assertIsNotNone(notification)
        self.assertIn('Test Event', notification.message)

    def test_send_event_update_notifications(self):
        """Test sending update notifications when event is modified"""
        # Create test event
        test_event = Event(
            name='Test Event',
            date=date.today().strftime('%Y-%m-%d'),
            description='Test description',
            location='Somewhere'
        )
        test_event.assigned_users.append(self.test_user)
        db.session.add(test_event)
        db.session.commit()

        # Send update notifications
        send_event_update_notifications(test_event.id)

        # Verify update notification was created
        notification = Notification.query.filter_by(
            user_id=self.test_user.id,
            notif_type='update'
        ).first()
        self.assertIsNotNone(notification)
        self.assertIn('Test Event', notification.message)

if __name__ == '__main__':
    unittest.main()
