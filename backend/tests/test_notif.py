import unittest
from unittest.mock import patch, mock_open
import sys
sys.path.append('../')
from app import app
import json
from flask import Flask, session
from routes import load_notifications, save_notifications, get_notifications, delete_notification, send_reminder_notifications, send_event_update_notifications
from datetime import datetime, timedelta, date

class TestNotifications(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'testkey' # for session testing
        self.client = app.test_client() # create a test client
        self.client.testing = True

    @patch('routes.load_notifications')
    def test_get_notifications(self, mock_load_notifications):
        mock_load_notifications.return_value = {
            "1": [
                {
                    "id": "1",
                    "title": "Assignment",
                    "date": "11-22-63",
                    "message": "Event assigned: Beach Cleanup",
                    "type": "assignment",
                    "read": True
                }]}

        with self.client.session_transaction() as session:
            session['user_id'] = "1"

        response = self.client.get('/api/notifications')

        # Assert: Check response and data
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(len(json_data), 1)
        self.assertEqual(json_data[0]['message'], "Event assigned: Beach Cleanup")


    @patch('routes.load_notifications')
    @patch('routes.save_notifications')
    def test_delete_notification(self, mock_save_notifications, mock_load_notifications):
        mock_load_notifications.return_value = {
            "1": [
                {
                    "id": "1",
                    "title": "Assignment",
                    "date": "11-22-63",
                    "message": "Event assigned: Beach Cleanup",
                    "type": "assignment",
                    "read": True
                }]}

        with self.client.session_transaction() as session:
            session['user_id'] = "1"

        response = self.client.delete('/api/notifications', json={'notification_id': "1"})
        self.assertEqual(response.status_code, 204)
        mock_save_notifications.assert_called_once()
        saved_data = mock_save_notifications.call_args[0][0]
        self.assertEqual(saved_data['1'], [])  # Check that notification was deleted

    @patch('routes.load_notifications')
    @patch('routes.save_notifications')
    def test_send_assignment_notification_success(self, mock_save_notifications, mock_load_notifications):
        mock_load_notifications.return_value = {}  # No current notifications
        user_id = '1'
        event_name = 'Test Event'
        event_date = '2024-12-25'
        current_date = date.today().strftime("%Y-%m-%d")

        response = self.client.post('/api/send-assignment-notification', json={
            'userId': user_id,
            'eventName': event_name,
            'eventDate': event_date
        })

        # Asserts
        self.assertEqual(response.status_code, 200)
        mock_save_notifications.assert_called_once()
        saved_notifications = mock_save_notifications.call_args[0][0]
        self.assertIn(user_id, saved_notifications)
        self.assertEqual(saved_notifications[user_id][0]['message'], f"Event assigned: {event_name} on {event_date}")
        self.assertEqual(saved_notifications[user_id][0]['date'], current_date)


    @patch('routes.load_notifications')
    @patch('routes.save_notifications')
    @patch('routes.read_events_from_file')
    def test_send_reminder_notifications_success(self, mock_read_events, mock_save_notifications, mock_load_notifications):
        now = datetime.now()
        event_date = now + timedelta(hours=23)  # Event happening within 24 hours
        event_data = [{
            'name': 'Reminder Event',
            'date': event_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'assignedUsers': ['1']
        }]
        mock_read_events.return_value = event_data
        mock_load_notifications.return_value = {'1': []}

        # Call the function to send reminders
        send_reminder_notifications()

        # Asserts to ensure notifications are saved and the correct reminder message is sent
        mock_save_notifications.assert_called_once()
        saved_notifications = mock_save_notifications.call_args[0][0]
        self.assertIn('1', saved_notifications)
        self.assertEqual(saved_notifications['1'][0]['message'], f"Event Reminder: 'Reminder Event' is coming up in 24 hours!")

    @patch('routes.load_notifications')
    @patch('routes.save_notifications')
    @patch('routes.read_events_from_file')
    def test_send_event_update_notifications_success(self, mock_read_events, mock_save_notifications, mock_load_notifications):
        event_id = '1'
        event_data = {
            event_id: {
                'name': 'Updated Event',
                'assignedUsers': ['1']
            }
        }
        mock_read_events.return_value = event_data
        mock_load_notifications.return_value = {'1': []}
        current_date = date.today().strftime("%m-%d-%y")

        # Call the function to send update notifications
        send_event_update_notifications(event_id)

        # Check that notification is added and saved correctly
        mock_save_notifications.assert_called_once()
        saved_notifications = mock_save_notifications.call_args[0][0]
        self.assertIn('1', saved_notifications)
        self.assertEqual(saved_notifications['1'][0]['message'], "Event Update: 'Updated Event' has been updated, please check the event listing to view any changes.")
        self.assertEqual(saved_notifications['1'][0]['date'], current_date)

if __name__ == '__main__':
    unittest.main()
