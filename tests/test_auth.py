import unittest
from flask import json
import psycopg2
from base_test import TestBase

class TestAuth(TestBase):

    def test_register_valid_details(self):
        """ Tests creating a new user with valid details """
        test_user = {
            'username': 'TestUser',
            'email': 'Testemail',
            'password': 'password'
        }
        response = self.client.post('/api/v1/auth/register',
                                    data=json.dumps(test_user),
                                    content_type='application/json')
        self.assertIn('You registered successfully. Please login.',
                      str(response.data))
        self.assertEqual(response.status_code, 201)

    def test_register_existing_user(self):
        """ Tests creating a user with existing email """
        self.create_valid_user()
        response = self.create_valid_user()
        self.assertEqual(response.status_code, 409)
        self.assertIn("User already exists", str(response.data))