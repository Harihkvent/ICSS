document.addEventListener("DOMContentLoaded", () => {
  const chatOutput = document.getElementById("chat-output");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-btn");
  const toggleButton = document.getElementById("toggle-mode");

  toggleButton.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
  });

  sendButton.addEventListener("click", sendMessage);
  userInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") sendMessage();
  });

  function sendMessage() {
    const query = userInput.value.trim();
    if (!query) return;

    addMessage(query, "user");
    userInput.value = "";

    fetch("http://127.0.0.1:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
    })
    .then(data => addMessage(data.response, "bot"))
    .catch(error => {
        console.error("Fetch error:", error);
        addMessage("Error retrieving response!", "bot");
    });
}


  function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(sender === "user" ? "user-message" : "bot-message");
    messageDiv.textContent = text;
    chatOutput.appendChild(messageDiv);
    chatOutput.scrollTop = chatOutput.scrollHeight;
  }
});
