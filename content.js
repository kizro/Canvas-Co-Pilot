// Inject CSS for chat UI
const link = document.createElement('link');
link.href = chrome.runtime.getURL('chat.css'); // pointing to 'chat.css' in extension directory
link.type = 'text/css';
link.rel = 'stylesheet';
document.head.appendChild(link);

// Check if our chat UI is already present
if (!document.getElementById('chat-container')) {
    // Create chat container
    const chatContainer = document.createElement('div');
    chatContainer.id = 'chat-container';
    chatContainer.innerHTML = `
        <div id="chat-window"></div>
        <input type="text" id="user-input" placeholder="Type your message...">
        <button id="send-btn">Send</button>
    `;
    document.body.appendChild(chatContainer);

    // Add functionality (e.g., sending message on button click)
    document.getElementById('send-btn').addEventListener('click', sendMessage);
}

function sendMessage() {
    const userInputField = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    const userText = userInputField.value.trim();

    if (userText) {
        // Display the user's message in the chat window
        const userMessage = document.createElement('div');
        userMessage.textContent = `You: ${userText}`;
        userMessage.className = 'user-message';
        chatWindow.appendChild(userMessage);

        // Here, you can add the functionality to process the message and generate a response
        const responseMessage = document.createElement('div');
        responseMessage.textContent = `Co-Pilot: Echoing back "${userText}"`;
        responseMessage.className = 'response-message'; // Add class
        chatWindow.appendChild(responseMessage);

        // Clear the input field
        userInputField.value = '';
        
        // Ensure the chat window scrolls to the latest message
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
}

// Support sending message with Enter key
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault(); // Prevent the default action to avoid form submission
        sendMessage();
    }
});
