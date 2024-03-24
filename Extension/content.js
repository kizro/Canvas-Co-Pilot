//Content.js with backend integration
// Inject CSS for chat UI
let welcomeMessageDisplayed = false;
let chatHistoryContent = ""; // Holds the chat history HTML content
const link = document.createElement('link');
link.href = chrome.runtime.getURL('chat.css'); // pointing to 'chat.css' in the extension directory
link.type = 'text/css';
link.rel = 'stylesheet';
document.head.appendChild(link);
const faLink = document.createElement('link');
faLink.rel = 'stylesheet';
faLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css';
document.head.appendChild(faLink);


function toggleChat(minimize = false) {
    const chatContainer = document.getElementById('chat-container');
    if (minimize) {
        // Save current chat content and minimize
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow) {
            chatHistoryContent = chatWindow.innerHTML; // Save chat history
        }
        chatContainer.classList.add('minimized');
        chatContainer.innerHTML = '<i class="fa-solid fa-comments fa-lg"></i>'; 
    } else {
        // Check if it's time to expand
        if (chatContainer.classList.contains('minimized')) {
            chatContainer.classList.remove('minimized');
            rebuildChatUI();
            const chatWindow = document.getElementById('chat-window');
            if (!welcomeMessageDisplayed) {
                const welcomeMessageDiv = document.createElement('div');
                welcomeMessageDiv.className = 'welcome-message';
                welcomeMessageDiv.innerHTML = `
                <p>Hi, I'm Canvas Copilot. <span class="wave">👋</span></p>
                <p>I'm your 24/7 assistant for all things school.</p>
                <p>You can ask me about your assignments, deadlines, announcements, grades, quizzes, or any general questions!</p>
            `;
                chatWindow.appendChild(welcomeMessageDiv);
                welcomeMessageDisplayed = true;
            } else if (chatWindow) {
                chatWindow.innerHTML = '';
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
        <i class="fa-solid fa-comments fa-lg" id="header-logo" alt="Logo"></i> 
        <span>Canvas Copilot!</span>
            <button id="close-btn"><i class="fas fa-times"></i></button>
        </div>
        <div id="chat-window"></div>
        <div style="display: flex;"> <!-- Added flex container for input and button -->
            <input type="text" id="user-input" placeholder="Type your message...">
            <button id="send-btn">Send</button>
        </div>
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

        const welcomeMessageDiv = document.querySelector('.welcome-message');
        if (welcomeMessageDiv) {
            chatWindow.removeChild(welcomeMessageDiv);
            welcomeMessageDisplayed = true; // Update the flag to prevent showing the welcome message again
        }
        // Display user's message in the chat
        displayMessage(`You: ${userText}`, 'user-message');

        //Waiting Message
        const waitingMessageId = 'waiting-message';
        displayMessage('Waiting...', 'waiting-message waiting-message', waitingMessageId);

        // AJAX POST request to the Flask '/prompt' route
        fetch('http://127.0.0.1:6524/prompt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userText }),  // Send userText as JSON
        })
        .then(response => response.json())
        .then(data => {

            // Remove the "waiting..." message
            removeMessage(waitingMessageId);

            // Display the response from Flask backend
            displayMessage(`Co-Pilot: ${data.response}`, 'response-message');
        })
        .catch((error) => {
            // Remove the "waiting..." message
            removeMessage(waitingMessageId);

            //console.error('Error:', error);
            displayMessage("Error: Could not get a response.", 'response-message');
        });

        userInputField.value = ''; // Clear the input field
        chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the latest message
    }
}

// Your displayMessage function remains unchanged


function displayMessage(text, className, id = null) {
    const chatWindow = document.getElementById('chat-window');
    const message = document.createElement('div');
    message.textContent = text;
    message.className = className;
    if (id) message.id = id;  // Set the id if provided
    chatWindow.appendChild(message);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the latest message
}

function removeMessage(messageId) {
    const messageToRemove = document.getElementById(messageId);
    if (messageToRemove) {
        messageToRemove.parentNode.removeChild(messageToRemove);
    }
}

// Initial chat UI setup
if (!document.getElementById('chat-container')) {
    const chatContainer = document.createElement('div');
    chatContainer.id = 'chat-container';
    chatContainer.classList.add('minimized'); // Start minimized
    chatContainer.innerHTML = '<i class="fa-solid fa-comments fa-lg"></i>'; 
    document.body.appendChild(chatContainer);

    // Expand chat when the '+' button is clicked
    chatContainer.addEventListener('click', function() {
        toggleChat();
    });

    // After setting up the chat UI, trigger the function in the Flask app
   // fetch('http://127.0.0.1:6524/', { method: 'GET' })
     //   .then(() => console.log("Function triggered in Flask."))
      //  .catch(error => console.error('Error triggering the function:', error));
}
