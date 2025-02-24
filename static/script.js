// let chatHistory = [];

// const chatBox = document.getElementById('chatBox');
// const userInput = document.getElementById('userInput');

// function addMessage(message, isUser) {
//     const messageDiv = document.createElement('div');
//     messageDiv.classList.add('message');
//     messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
    
//     // Parse and format the message for markdown-like elements
//     messageDiv.innerHTML = formatMessage(message);
//     chatBox.appendChild(messageDiv);
//     chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to bottom
// }

// function formatMessage(message) {
//     // Simple markdown-like formatting
//     let formatted = message
//         .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
//         .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italics
//         .replace(/---/g, '<hr>') // Horizontal line
//         .replace(/^- (.*)$/gm, '<li>$1</li>') // List items (simple)
//         .replace(/(?:\r\n|\r|\n)/g, '<br>'); // Line breaks
    
//     // Wrap lists in <ul> if they exist
//     if (formatted.includes('<li>')) {
//         formatted = `<ul>${formatted}</ul>`;
//     }
    
//     return formatted;
// }

// async function sendMessage() {
//     const message = userInput.value.trim();
//     if (!message) return;

//     // Add user message to chat and history
//     addMessage(message, true);
//     chatHistory.push({ role: 'user', content: message });
//     userInput.value = ''; // Clear input

//     // Send message to backend
//     try {
//         const response = await fetch('/chat', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify({ message: message }),
//         });

//         const data = await response.json();
//         if (data.error) {
//             addMessage('Error: ' + data.error, false);
//         } else {
//             addMessage(data.response, false);
//             chatHistory.push({ role: 'assistant', content: data.response });
            
//             // Update chat box with full history for context (optional visual)
//             updateChatHistoryDisplay();
//         }
//     } catch (error) {
//         addMessage('Error: Unable to reach the server', false);
//         console.error(error);
//     }
// }

// function updateChatHistoryDisplay() {
//     // This function could be used to refresh the chat box with the full history
//     // For now, we rely on addMessage, but this can be expanded for visual history
//     chatBox.innerHTML = ''; // Clear current display
//     chatHistory.forEach(msg => {
//         addMessage(msg.content, msg.role === 'user');
//     });
// }

// // Send message on Enter key press
// userInput.addEventListener('keypress', (e) => {
//     if (e.key === 'Enter') {
//         sendMessage();
//     }
// });

// // Load initial history (if any) when the page loads
// window.onload = () => {
//     // If you want to persist history across sessions, you'd load it here (e.g., from localStorage or a backend)
//     if (chatHistory.length > 0) {
//         updateChatHistoryDisplay();
//     }
// };

let chatHistory = [];

const chatBox = document.getElementById('chatBox');
const userInput = document.getElementById('userInput');

function addMessage(message, isUser) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', isUser ? 'user-message' : 'bot-message');
    messageDiv.innerHTML = formatMessage(message);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function formatMessage(message) {
    return message
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/^- (.*)$/gm, '<li>$1</li>') // Lists
        .replace(/(?:\r\n|\r|\n)/g, '<br>') // Line breaks
        .replace(/(<li>.*<\/li>)/g, '<ul>$1</ul>'); // Wrap lists
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, true);
    chatHistory.push({ role: 'user', content: message });
    userInput.value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message }),
        });

        const data = await response.json();
        if (data.error) {
            addMessage(`Oops! Something went wrong: ${data.error}. Try again!`, false);
        } else {
            addMessage(data.response, false);
            chatHistory.push({ role: 'assistant', content: data.response });
        }
    } catch (error) {
        addMessage('Oops! Can’t reach the server right now. Please try again.', false);
        console.error(error);
    }
}

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});