---

# Flask Chat Application

This is a real-time chat application built using Flask, SocketIO, and MongoDB. The app allows users to sign up, sign in, create chat rooms, and send messages in real-time. It leverages Flask-Login for user authentication and Flask-SocketIO for real-time communication between users.

## Features

- **User Authentication**: Users can sign up, sign in, and log out using email and password.
- **Real-time Messaging**: Users can create and join chat rooms, and send/receive messages in real time.
- **MongoDB**: User data (username, password, and email) is stored in a MongoDB database.
- **Flask-SocketIO**: Real-time updates for message exchange and room joining.

## Requirements

Ensure the following libraries are installed:

- `Flask`: For the web framework.
- `Flask-SocketIO`: For real-time communication.
- `Flask-Bcrypt`: For secure password hashing.
- `Flask-Login`: For managing user sessions.
- `pymongo`: For interacting with MongoDB.
- `python-dotenv` (optional but recommended for managing environment variables securely).

You can install all the dependencies by running:

```bash
pip install flask flask-socketio flask-bcrypt flask-login pymongo python-dotenv
```

You also need to have MongoDB running on your local machine or use a remote MongoDB service.

## Setup Instructions

1. **Install Dependencies**: 
   Ensure that you have Python and the necessary libraries installed. Run the following command to install the required dependencies:

   ```bash
   pip install flask flask-socketio flask-bcrypt flask-login pymongo python-dotenv
   ```

2. **MongoDB Setup**:
   The app uses MongoDB for storing user data. Ensure you have MongoDB installed and running locally or use a remote MongoDB instance. The app is configured to connect to `mongodb://localhost:27017/chatapp`.

3. **Environment Configuration**:
   For production, you should use a `.env` file to store sensitive information, such as the `SECRET_KEY`. The current app uses a placeholder `your_secret_key`, which should be changed to a secure key.

4. **Run the Flask Application**:
   To run the application, navigate to the directory where the `app.py` file is located and run:

   ```bash
   python app.py
   ```

   This will start the Flask server, and the app should be accessible at `http://127.0.0.1:5000/` on your local machine.

## App Routes

- **`/`**: Home page, redirects to the chat page if logged in.
- **`/features`**: Displays the features of the app.
- **`/about`**: Displays information about the app.
- **`/contacts`**: Displays contact information.
- **`/signup`**: User registration page.
- **`/signin`**: User login page.
- **`/profile`**: User profile page (accessible after login).
- **`/chat`**: Chat room page (accessible after login).
- **`/create_room`**: Create a new chat room.
- **`/join_room`**: Join an existing chat room by room ID.
- **`/logout`**: Logs the user out and redirects to the home page.

## Real-time Chat

- **SocketIO Integration**: The app uses `Flask-SocketIO` to manage real-time communication. Users can join chat rooms and send messages instantly.
- **Room ID Generation**: A random room ID is generated when creating a new room. Users can join rooms by entering the room ID.

## SocketIO Events

- **`join`**: Emitted when a user joins a room. Sends a system message to the room that the user has joined.
- **`send_message`**: Emitted when a user sends a message to the room.

## User Authentication

The application uses `Flask-Login` to manage user sessions:

- Users can sign up with a username, email, and password.
- Passwords are hashed using `Flask-Bcrypt` for secure storage.
- Users can log in using their credentials, and the session will persist until they log out.

## MongoDB Schema

The MongoDB collection for users (`chatapp.users`) contains the following fields:

- `username`: The username of the user.
- `password`: The hashed password.
- `email`: The email address of the user.

## Troubleshooting

- **MongoDB Connection**: Ensure MongoDB is running locally or use a cloud-based MongoDB service. If you're using a remote database, update the MongoDB connection string in the code.
- **SocketIO**: Ensure your environment supports WebSockets. If you face issues, check for any firewall or proxy settings blocking WebSocket communication.

## Security Considerations

- **Sensitive Information**: Use environment variables (e.g., in a `.env` file) to store sensitive data such as `SECRET_KEY` and MongoDB connection strings.
- **Password Storage**: Passwords are securely hashed using `Flask-Bcrypt` before being stored in the database.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
