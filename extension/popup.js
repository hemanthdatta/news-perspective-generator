// Format markdown text
function formatText(text) {
    return marked.parse(text);
}

// Show/hide loading spinner
function toggleLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.add('active');
    } else {
        loading.classList.remove('active');
    }
}

// Show error message
function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4';
    errorDiv.textContent = message;
    
    const results = document.getElementById('results');
    results.innerHTML = '';
    results.appendChild(errorDiv);
    toggleLoading(false);
}

// Add message to chat
function addMessageToChat(type, message) {
    const chatHistory = document.getElementById('chat-history');
    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${type === 'user' ? 'justify-end' : 'justify-start'} mb-2`;
    
    const messageContent = document.createElement('div');
    messageContent.className = `max-w-[80%] rounded-lg p-3 ${
        type === 'user' 
            ? 'bg-blue-500 text-white' 
            : type === 'error'
            ? 'bg-red-100 text-red-700'
            : 'bg-gray-100 text-gray-800'
    }`;
    messageContent.innerHTML = type === 'ai' ? formatText(message) : message;
    
    messageDiv.appendChild(messageContent);
    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

// Load suggested questions
async function loadSuggestedQuestions() {
    try {
        const response = await fetch('http://localhost:8000/suggested_questions', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            console.error('Error:', data.error);
            return;
        }
        
        const container = document.getElementById('suggested-questions');
        container.innerHTML = '';
        
        const heading = document.createElement('div');
        heading.className = 'text-gray-600 mb-3';
        heading.textContent = 'Suggested Questions:';
        container.appendChild(heading);
        
        data.questions.forEach(question => {
            const button = document.createElement('button');
            button.className = 'px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-full text-sm font-medium transition-colors mb-2 mr-2';
            button.textContent = question;
            button.onclick = () => askSuggestedQuestion(question);
            container.appendChild(button);
        });
        
        container.classList.remove('hidden');
    } catch (error) {
        console.error('Error loading suggested questions:', error);
        showError('Failed to load suggested questions. Please try again.');
    }
}

// Ask a suggested question
function askSuggestedQuestion(question) {
    document.getElementById('chat-input').value = question;
    sendQuestion();
}

// Send a question
async function sendQuestion() {
    const input = document.getElementById('chat-input');
    const question = input.value.trim();
    
    if (!question) return;
    
    try {
        addMessageToChat('user', question);
        input.value = '';
        
        const response = await fetch('http://localhost:8000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            addMessageToChat('error', `⚠️ ${data.error}`);
            return;
        }
        
        addMessageToChat('ai', data.response);
        
    } catch (error) {
        console.error('Error sending question:', error);
        addMessageToChat('error', '⚠️ An error occurred while processing your question');
    }
}

// Analyze the current page
async function analyzePage() {
    try {
        // Get current tab URL
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        const url = tab.url;
        
        toggleLoading(true);
        document.getElementById('results').innerHTML = '';
        document.getElementById('suggested-questions').innerHTML = '';
        
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ url, perspective: 'all' }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.error) {
            showError(data.error);
            return;
        }
        
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';
        
        Object.entries(data).forEach(([perspective, analysis]) => {
            const card = document.createElement('div');
            card.className = 'bg-white rounded-lg shadow-lg p-6 mb-6';
            card.innerHTML = `
                <h3 class="text-xl font-bold mb-4 capitalize">${perspective} Perspective</h3>
                <div class="prose max-w-none">${formatText(analysis)}</div>
            `;
            resultsDiv.appendChild(card);
        });
        
        await loadSuggestedQuestions();
        
    } catch (error) {
        console.error('Error analyzing page:', error);
        showError('An error occurred while analyzing the article. Make sure the server is running on localhost:8000');
    } finally {
        toggleLoading(false);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    // Analyze button
    document.getElementById('analyze-page').addEventListener('click', analyzePage);
    
    // Chat input
    const chatInput = document.getElementById('chat-input');
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendQuestion();
        }
    });
});
