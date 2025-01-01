# chat/__init__.py

from flask_socketio import SocketIO
from .logic import handle_set_username, handle_message, handle_disconnect

socketio = SocketIO()

def register_socket_events(app):
    """Register the WebSocket events with the Flask-SocketIO instance."""
    socketio.init_app(app)

    # Event handlers
    @socketio.on('set_username')
    def on_set_username(username):
        handle_set_username(username)

    @socketio.on('message')
    def on_message(msg):
        handle_message(msg)

    @socketio.on('disconnect')
    def on_disconnect():
        handle_disconnect()
