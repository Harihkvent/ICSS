// Dark/Light Mode Toggle
const toggleButton = document.getElementById('toggle-mode');
toggleButton.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');
});

// Chatbot Functionality
const sendButton = document.getElementById('send-btn');
const chatOutput = document.getElementById('chat-output');
const userInput = document.getElementById('user-input');

sendButton.addEventListener('click', function () {
  const query = userInput.value.trim();
  if (query) {
    const userMessage = createMessage(query, 'user');
    chatOutput.appendChild(userMessage);

    const response = getResponse(query);
    const botMessage = createMessage(response, 'bot');
    chatOutput.appendChild(botMessage);

    userInput.value = '';
    chatOutput.scrollTop = chatOutput.scrollHeight; // Scroll to bottom after new message
  }
});

function createMessage(text, sender) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
  messageDiv.textContent = text;
  return messageDiv;
}

function getResponse(query) {
  if (query.includes('hello')) return 'Hi! How can I assist you today?';
  if (query.includes('issue')) return 'I am sorry to hear that. Could you please provide more details about the issue?';
  if (query.includes('contact')) return 'You can reach our support team at support@company.com';
  if (query.includes('hours')) return 'Our support team is available from 9 AM to 6 PM, Monday to Friday.';
  return 'I\'m sorry, I didn\'t understand that. Could you please rephrase your question?';
}
