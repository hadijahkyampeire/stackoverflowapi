import unittest
import json
from api.database import Database as db
from instance import config
from . import base
from api import app


class TestRide(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

        with app.app_context():
            connection = db()
            connection.drop_tables()
            connection.create_tables()

    def test_register_user(self):
        register_response = base.register_user(self)
        data = json.loads(register_response.data.decode())
        self.assertEqual(register_response.status_code, 201)

    def test_login_user(self):
        base.register_user(self)
        login_response = base.login_user(self)
        result = json.loads(login_response.data.decode())
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result['message'], "You logged in successfully.")

    def tearDown(self):
        with app.app_context():
            connection = db()
            connection.drop_tables()
            connection.create_tables()