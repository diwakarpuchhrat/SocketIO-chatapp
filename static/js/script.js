const socket = io(); 

let username;


while (!username) {
    username = prompt("What is your name?");
}
socket.emit('set_username', username); 

const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');


sendButton.addEventListener('click', () => {
    const message = messageInput.value.trim();
    if (message !== '') {
        socket.send(message); 
        messageInput.value = ''; 
    }
});


socket.on('message', (msg) => {
    const messageElement = document.createElement('div');
    messageElement.textContent = msg;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; 
});


socket.on('user_connected', (msg) => {
    const notificationElement = document.createElement('div');
    notificationElement.textContent = msg;
    notificationElement.style.color = 'green';
    chatBox.appendChild(notificationElement);
    chatBox.scrollTop = chatBox.scrollHeight;
});

socket.on('user_disconnected', (msg) => {
    const notificationElement = document.createElement('div');
    notificationElement.textContent = msg;
    notificationElement.style.color = 'red';
    chatBox.appendChild(notificationElement);
    chatBox.scrollTop = chatBox.scrollHeight;
});
