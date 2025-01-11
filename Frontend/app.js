// Global Variables
let userLoggedIn = false;
let username = '';

// Simulate a user login check (can be replaced with actual API later)
const validateLogin = (username, password) => {
    // For simplicity, let's assume the username is 'user' and password is 'password'
    return username === 'user' && password === 'password';
};

// Handle login
document.getElementById('login-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    if (validateLogin(user, pass)) {
        userLoggedIn = true;
        username = user;
        localStorage.setItem('username', username); // Store username in localStorage
        window.location.href = 'index.html'; // Redirect to the chat page
    } else {
        document.getElementById('error-message').innerText = 'Invalid username or password';
    }
});

// Display the user name and login state
window.onload = () => {
    if (userLoggedIn || localStorage.getItem('username')) {
        username = localStorage.getItem('username');
        document.getElementById('user-name').innerText = username;
        document.getElementById('logout-btn').style.display = 'inline';
    }
};

// Handle sending a message
document.getElementById('send-btn')?.addEventListener('click', function() {
    const messageInput = document.getElementById('query-input').value;
    if (messageInput.trim() !== '') {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.innerHTML = `<strong>${username}</strong>: ${messageInput}`;
        document.getElementById('messages').appendChild(messageDiv);
        document.getElementById('query-input').value = ''; // Clear input
        document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight; // Scroll to the latest message
    }
});

// Handle logout
document.getElementById('logout-btn')?.addEventListener('click', function() {
    userLoggedIn = false;
    localStorage.removeItem('username');
    window.location.href = 'login.html'; // Redirect to login
});
