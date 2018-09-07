import datetime
import json
from api.models import User, Questions, Answers

valid_user = {"username":"haddy","email":"haddy1@mail.com", "password":"123456"}
login_user={"email":"haddy1@mail.com", "password":"123456"}

# user_with_missing_values = User(email="haddy1@mail.com")
# user_with_invalid_email = User(username="haddy2", email="", password="123")
# user_with_wrong_password = User(username="haddy", email="sample1@mail.com", password="34")
# different_user_logs_in = User(email="sample1@mail.com", password="hhd")
# valid_question = Questions(title="Math", description="what is math")

def register_user(self):
    """method sends a request to register a user
       parameters username,email,password,confirm_password
       returns json response with users token"""

    return self.app.post('/api/v1/auth/register', data=json.dumps(valid_user), content_type='application/json')


def login_user(self, user):
    """method login_user sends a request to login user
       parameters email,password
       returns json response with users token"""

    return self.app.post('/api/v1/auth/login', data=json.dumps(login_user),
                         content_type='application/json')

