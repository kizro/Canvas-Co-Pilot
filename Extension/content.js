// Inject CSS for chat UI
let chatHistoryContent = ""; // Holds the chat history HTML content
const link = document.createElement('link');
link.href = chrome.runtime.getURL('chat.css'); // pointing to 'chat.css' in the extension directory
link.type = 'text/css';
link.rel = 'stylesheet';
document.head.appendChild(link);

function toggleChat(minimize = false) {
    const chatContainer = document.getElementById('chat-container');
    if (minimize) {
        // Save current chat content and minimize
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow) {
            chatHistoryContent = chatWindow.innerHTML; // Save chat history
        }
        chatContainer.classList.add('minimized');
        chatContainer.innerHTML = '+'; // Show '+' sign
    } else {
        // Check if it's time to expand
        if (chatContainer.classList.contains('minimized')) {
            chatContainer.classList.remove('minimized');
            rebuildChatUI();
            const chatWindow = document.getElementById('chat-window');
            if (chatWindow) {
                chatWindow.innerHTML = chatHistoryContent; // Restore chat history
            }
        }
    }
}

function rebuildChatUI() {
    const chatContainer = document.getElementById('chat-container');
    // Clear '+' sign and prepare to add UI elements, without overwriting chat history
    chatContainer.innerHTML = `
        <div id="chat-header">
            <span>Canvas Co Pilot</span>
            <button id="close-btn">X</button>
        </div>
        <div id="chat-window"></div>
        <input type="text" id="user-input" placeholder="Type your message...">
        <button id="send-btn">Send</button>
    `;

    // Append the saved chat history if available
    const chatWindow = document.getElementById('chat-window');
    chatWindow.innerHTML = chatHistoryContent;

    // Logic to minimize chat when close button is clicked
    document.getElementById('close-btn').addEventListener('click', function(event) {
        toggleChat(true);
        event.stopPropagation(); // Prevent triggering the container's click event
    });

    document.getElementById('send-btn').addEventListener('click', function(event) {
        sendMessage();
        event.stopPropagation(); // Prevent triggering the container's click event
    });

    document.getElementById('user-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault(); // Prevent form submission
            sendMessage();
            e.stopPropagation(); // Prevent triggering the container's click event
        }
    });
}

function sendMessage() {
    const userInputField = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    const userText = userInputField.value.trim();

    if (userText) {
        // Display user's message and echo back
        displayMessage(userText, 'user-message');
        displayMessage(`Co-Pilot: Echoing back "${userText}"`, 'response-message');

        userInputField.value = ''; // Clear input field
        chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to latest message
    }
}

function displayMessage(text, className) {
    const chatWindow = document.getElementById('chat-window');
    const message = document.createElement('div');
    message.textContent = text;
    message.className = className;
    chatWindow.appendChild(message);
}

// Initial chat UI setup
if (!document.getElementById('chat-container')) {
    const chatContainer = document.createElement('div');
    chatContainer.id = 'chat-container';
    chatContainer.classList.add('minimized'); // Start minimized
    chatContainer.textContent = '+'; // Show '+' sign
    document.body.appendChild(chatContainer);

    // Expand chat when the '+' button is clicked
    chatContainer.addEventListener('click', function() {
        toggleChat();
    });
}
