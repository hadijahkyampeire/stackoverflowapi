
class User():
    """class for users"""

    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password


class Questions():
    """class for questions"""

    def __init__(self, question_id, title, description):
        self.id = question_id
        self.title = title
        self.description = description

class Answers():
    """class for answers"""

    def __init__(self, answer_id, reply):
        self.id = answer_id
        self.reply = reply


