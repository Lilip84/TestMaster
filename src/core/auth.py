from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.username = "admin"
    
    @staticmethod
    def get(user_id):
        return User(user_id)