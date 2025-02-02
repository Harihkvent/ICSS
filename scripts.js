document.addEventListener("DOMContentLoaded", () => {
  const chatOutput = document.getElementById("chat-output");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-btn");
  const toggleButton = document.getElementById("toggle-mode");
  const micButton = document.createElement("button");
  micButton.textContent = "🎤";
  micButton.id = "mic-btn";
  document.getElementById("chat-container").appendChild(micButton);

  let voiceInputUsed = false;

  
  // Language Selection Dropdown
  const languageSelect = document.createElement("select");
  languageSelect.id = "language-select";
  const languages = {
    "en-US": "English",
    "hi-IN": "Hindi",
    "te-IN": "Telugu",
    "es-ES": "Spanish",
    "fr-FR": "French",
    "de-DE": "German",
  };

  for (const [code, name] of Object.entries(languages)) {
    let option = document.createElement("option");
    option.value = code;
    option.textContent = name;
    languageSelect.appendChild(option);
  }
  document.getElementById("chat-container").appendChild(languageSelect);

  sendButton.addEventListener("click", () => {
    voiceInputUsed = false;
    sendMessage();
  });

  micButton.addEventListener("click", startVoiceInput);

  userInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
      voiceInputUsed = false;
      sendMessage();
    }
  });

  function sendMessage() {
    const query = userInput.value.trim();
    if (!query) return;

    addMessage(query, "user");
    userInput.value = "";

    fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    })
      .then((response) => {
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        addMessage(data.response, "bot");
        if (voiceInputUsed) speakText(data.response);
      })
      .catch((error) => {
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

  function startVoiceInput() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = languageSelect.value;
    recognition.start();

    recognition.onresult = (event) => {
      const voiceText = event.results[0][0].transcript;
      userInput.value = voiceText;
      voiceInputUsed = true;
      sendMessage();
    };

    recognition.onerror = (event) => {
      console.error("Speech Recognition Error", event.error);
    };
  }

  function speakText(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = languageSelect.value;
    speechSynthesis.speak(speech);
  }
});
