from flask import session
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson.objectid import ObjectId

bcrypt = Bcrypt()
mongo = None
login_manager = LoginManager()

def init_app(app):
    """Initialize app with MongoDB, bcrypt, and Flask-Login."""
    global mongo
    mongo = PyMongo(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Load the user from MongoDB by user_id."""
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user:
        return User(user)
    return None

class User(UserMixin):
    """User class to integrate with Flask-Login."""
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']

def create_user(username, password, email):
    """Create a new user and store it in MongoDB."""
    # Check if user already exists
    if mongo.db.users.find_one({'username': username}):
        return False  # Username already taken
    
    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Insert the user into MongoDB
    mongo.db.users.insert_one({
        'username': username,
        'password': hashed_password,
        'email': email
    })
    print(f"User created: {username}")  # Debugging statement
    return True

def check_user(username, password):
    """Check if the username exists and the password matches."""
    user = mongo.db.users.find_one({'username': username})
    if user:
        print(f"Found user: {user}")  # Debugging print statement
        if bcrypt.check_password_hash(user['password'], password):
            return User(user)  # Return User object for Flask-Login
    return None
