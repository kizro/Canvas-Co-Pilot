<<<<<<< HEAD
=======
//Content.js with backend integration
>>>>>>> 261dd2b2ec2e3ad3e21637b29e71be2a38cc07c6
// Inject CSS for chat UI
let chatHistoryContent = ""; // Holds the chat history HTML content
const link = document.createElement('link');
link.href = chrome.runtime.getURL('chat.css'); // pointing to 'chat.css' in the extension directory
link.type = 'text/css';
link.rel = 'stylesheet';
document.head.appendChild(link);
<<<<<<< HEAD
const faLink = document.createElement('link');
faLink.rel = 'stylesheet';
faLink.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css';
document.head.appendChild(faLink);

=======
>>>>>>> 261dd2b2ec2e3ad3e21637b29e71be2a38cc07c6

function toggleChat(minimize = false) {
    const chatContainer = document.getElementById('chat-container');
    if (minimize) {
        // Save current chat content and minimize
        const chatWindow = document.getElementById('chat-window');
        if (chatWindow) {
            chatHistoryContent = chatWindow.innerHTML; // Save chat history
        }
        chatContainer.classList.add('minimized');
<<<<<<< HEAD
        chatContainer.innerHTML = '<i class="fa-solid fa-comments fa-lg"></i>'; 
=======
        chatContainer.innerHTML = '+'; // Show '+' sign
>>>>>>> 261dd2b2ec2e3ad3e21637b29e71be2a38cc07c6
    } else {
        // Check if it's time to expand
        if (chatContainer.classList.contains('minimized')) {
            chatContainer.classList.remove('minimized');
            rebuildChatUI();
            const chatWindow = document.getElementById('chat-window');
            if (chatWindow) {
                chatWindow.innerHTML = chatHistoryContent; // Restore chat history
<<<<<<< HEAD
                chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to latest message
=======
>>>>>>> 261dd2b2ec2e3ad3e21637b29e71be2a38cc07c6
            }
        }
    }
}

function rebuildChatUI() {
    const chatContainer = document.getElementById('chat-container');
    // Clear '+' sign and prepare to add UI elements, without overwriting chat history
    chatContainer.innerHTML = `
        <div id="chat-header">
<<<<<<< HEAD
        <i class="fa-solid fa-comments fa-lg" id="header-logo" alt="Logo"></i> 
        <span>Canvas Co Pilot</span>
            <button id="close-btn"><i class="fas fa-times"></i></button>
        </div>
        <div id="chat-window"></div>
        <div style="display: flex;"> <!-- Added flex container for input and button -->
            <input type="text" id="user-input" placeholder="Type your message...">
            <button id="send-btn">Send</button>
        </div>
=======
            <span>Canvas Co Pilot</span>
            <button id="close-btn">X</button>
        </div>
        <div id="chat-window"></div>
        <input type="text" id="user-input" placeholder="Type your message...">
        <button id="send-btn">Send</button>
>>>>>>> 261dd2b2ec2e3ad3e21637b29e71be2a38cc07c6
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
<<<<<<< HEAD
        // Display user's message and echo back
        displayMessage(userText, 'user-message');
        displayMessage(`Co-Pilot: Echoing back "${userText}"`, 'response-message');

        userInputField.value = ''; // Clear input field
        chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to latest message
    }
}

=======
        // Display user's message in the chat
        displayMessage(userText, 'user-message');

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
            // Display the response from Flask backend
            displayMessage(`Co-Pilot: ${data.response}`, 'response-message');
        })
        .catch((error) => {
            console.error('Error:', error);
            displayMessage("Error: Could not get a response.", 'response-message');
        });

        userInputField.value = ''; // Clear the input field
        chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the latest message
    }
}

// Your displayMessage function remains unchanged


>>>>>>> 261dd2b2ec2e3ad3e21637b29e71be2a38cc07c6
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
<<<<<<< HEAD
    chatContainer.innerHTML = '<i class="fa-solid fa-comments fa-lg"></i>'; 
=======
    chatContainer.textContent = '+'; // Show '+' sign
>>>>>>> 261dd2b2ec2e3ad3e21637b29e71be2a38cc07c6
    document.body.appendChild(chatContainer);

    // Expand chat when the '+' button is clicked
    chatContainer.addEventListener('click', function() {
        toggleChat();
    });
<<<<<<< HEAD
}
=======

    // After setting up the chat UI, trigger the function in the Flask app
   // fetch('http://127.0.0.1:6524/', { method: 'GET' })
     //   .then(() => console.log("Function triggered in Flask."))
      //  .catch(error => console.error('Error triggering the function:', error));
}
>>>>>>> 261dd2b2ec2e3ad3e21637b29e71be2a38cc07c6
