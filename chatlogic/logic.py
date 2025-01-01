# chat/logic.py

from flask_socketio import send, emit
from flask import request

users = {}

def handle_set_username(username):
    """Set the username for the user"""
    users[request.sid] = username
    print(f"User connected: {username} (SID: {request.sid})")
    emit('user_connected', f"{username} has joined the chat!", broadcast=True)

def handle_message(msg):
    """Handle messages sent by users"""
    username = users.get(request.sid, "Anonymous")
    formatted_message = f"{username}: {msg}"
    print(formatted_message)
    send(formatted_message, broadcast=True)

def handle_disconnect():
    """Handle when a user disconnects"""
    username = users.pop(request.sid, "Anonymous")
    print(f"User disconnected: {username} (SID: {request.sid})")
    emit('user_disconnected', f"{username} has left the chat.", broadcast=True)
