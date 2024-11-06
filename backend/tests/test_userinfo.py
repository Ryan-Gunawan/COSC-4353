import unittest
from app import app, db
import json
import os
import sys
sys.path.append('../')
from flask import Flask, session
# from routes import get_userinfo, update_userinfo
from unittest.mock import patch, MagicMock
from models import User

class TestUserInfo(unittest.TestCase):
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
        db.session.commit()

        # Store test user data for comparison
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
    
    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_get_userinfo(self): 
        with self.client.session_transaction() as sess:
            sess['user_id'] = self.test_user.id

        response = self.client.get('/api/userprofile')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)

        self.assertEqual(data.get('email'), self.test_user_data['email'])
        self.assertEqual(data.get('fullname'), self.test_user_data['fullname'])
        self.assertEqual(data.get('city'), self.test_user_data['city'])

    def test_update_userinfo(self):
        updated_data = {
            'fullname':'Real Full Name',
            'address1': '100 Harvey Drive'
        }

        response = self.client.put(f'/api/userprofile/{self.test_user.id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['msg'], 'User info updated successfully')

        # Fetch the updated user and verify changes
        updated_user = User.query.get(self.test_user.id)
        self.assertEqual(updated_user.fullname, 'Real Full Name')
        self.assertEqual(updated_user.address1, '100 Harvey Drive')

if __name__ == '__main__':
    unittest.main()
