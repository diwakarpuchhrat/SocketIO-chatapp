from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_socketio import SocketIO, join_room
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import random
import string

# Initialize Flask app and configurations
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ensure this is kept secret and secure in a production environment
socketio = SocketIO(app)
bcrypt = Bcrypt(app)

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/chatapp')
db = client['chatapp']
users_collection = db['users']

# Flask-Login setup
login_manager = LoginManager(app)
login_manager.login_view = 'signin'


# Room storage
rooms = {}

# Generate random room ID
def generate_room_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=4))


# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({'_id': user_id})
    if user:
        return User(user['username'])
    return None

# User class for Flask-Login
class User:
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username


# Routes for Signup, Signin, and Profile
@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat'))
    return render_template('landing.html')

@app.route('/features', methods=['GET'])
def features():
    return render_template('features.html')
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
@app.route('/contacts', methods=['GET'])
def contacts():
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve the form data
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords don't match", 'error')
            return redirect(url_for('signup'))

        # Check if the username already exists
        if users_collection.find_one({'username': username}):
            flash("Username already exists", 'error')
            return redirect(url_for('signup'))

        # Encrypt the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert the new user into the database
        users_collection.insert_one({'username': username, 'password': hashed_password, 'email': email})

        # Flash success message and redirect to signin page
        flash("Account created successfully! Please sign in.", 'success')
        return redirect(url_for('signin'))

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users_collection.find_one({'username': username})
        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            flash("Welcome back!", 'success')
            return redirect(url_for('chat'))
        flash("Invalid credentials. Please try again.", 'error')
        return redirect(url_for('signin'))

    return render_template('signin.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', username=current_user.username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('username', None)
    flash("You have been logged out.", 'success')
    return redirect(url_for('signin'))


# Chat Room routes
@app.route('/chat')
# @login_required
def chat():
    username = session['username']
    room_id = session.get('room_id')
    return render_template('chat.html', username=username, room_id=room_id)


@app.route('/create_room', methods=['POST'])
def create_room():
    username = session.get('username')
    if not username:
        return redirect('/signin')

    room_id = generate_room_id()
    rooms[room_id] = {'members': [username]}
    session['room_id'] = room_id
    return redirect('/chat')


@app.route('/join_room', methods=['POST'])
def join_room_view():
    room_id = request.form['room_id']
    username = session.get('username')
    if not username:
        return redirect('/signin')

    if room_id in rooms:
        rooms[room_id]['members'].append(username)
        session['room_id'] = room_id
        return redirect('/chat')
    return 'Room not found', 404


@app.route('/logout', methods=['GET','POST'])
def leave_chat():
    session.pop('room_id', None)
    session.pop('username', None)
    return redirect('/')


# SocketIO events
@socketio.on('join')
def on_join(data):
    username = session.get('username')
    room = data['room']
    join_room(room)
    socketio.emit('message', {'user': 'System', 'message': f"{username} has joined the room!"}, to=room)


@socketio.on('send_message')
def handle_message(data):
    room = session.get('room_id')
    message = data['message']
    username = session.get('username')
    socketio.emit('message', {'user': username, 'message': message}, room=room)


# Run the app
if __name__ == '__main__':
    socketio.run(app, debug=True)
