// Frontend JavaScript for Kyosan Ethics Engine
// ©sanjivakyosan
// Created by Sanjiva Kyosan

const API_BASE_URL = window.location.origin || '';

// DOM Elements - will be initialized after DOM loads
let userInput, processBtn, clearBtn, outputContainer, analysisContainer, analysisContent;
let statusIndicator, statusText, processingTime, processingLevel;
let footerSystems, systemsList;
let aiStatusLight;
let conversationNameInput, saveConversationBtn, loadConversationBtn, newConversationBtn, clearConversationBtn;
let toggleApiEndpointsBtn, toggleActiveSystemsBtn;
let followUpInput, followUpBtn, followUpSection, followUpConversation;

// Conversation state
let currentConversationId = null;
let conversationHistory = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Query all DOM elements
    userInput = document.getElementById('user-input');
    processBtn = document.getElementById('process-btn');
    clearBtn = document.getElementById('clear-btn');
    outputContainer = document.getElementById('output-container');
    analysisContainer = document.getElementById('analysis-container');
    analysisContent = document.getElementById('analysis-content');
    statusIndicator = document.getElementById('status-indicator');
    statusText = document.getElementById('status-text');
    processingTime = document.getElementById('processing-time');
    processingLevel = document.getElementById('processing-level');
    aiStatusLight = document.getElementById('ai-status-light');
    footerSystems = document.getElementById('footer-systems');
    systemsList = document.getElementById('systems-list');
    toggleApiEndpointsBtn = document.getElementById('toggle-api-endpoints');
    toggleActiveSystemsBtn = document.getElementById('toggle-active-systems');
    followUpInput = document.getElementById('follow-up-input');
    followUpBtn = document.getElementById('follow-up-btn');
    followUpSection = document.getElementById('follow-up-section');
    followUpConversation = document.getElementById('follow-up-conversation');
    conversationNameInput = document.getElementById('conversation-name');
    saveConversationBtn = document.getElementById('save-conversation-btn');
    loadConversationBtn = document.getElementById('load-conversation-btn');
    newConversationBtn = document.getElementById('new-conversation-btn');
    clearConversationBtn = document.getElementById('clear-conversation-btn');
    
    // Verify critical elements exist
    if (!userInput || !processBtn || !outputContainer || !statusText || !statusIndicator) {
        console.error('Critical DOM elements missing!');
        if (outputContainer) {
            outputContainer.innerHTML = '<div style="color: #f44336;"><strong>Error:</strong> Critical UI elements not found. Please refresh the page.</div>';
        }
        return;
    }
    
    checkHealth();
    loadSystemStatus();
    setupEventListeners();
    
    // Initialize AI status as connected (will be updated by health check)
    if (aiStatusLight) {
        updateAIStatus(true);
    }
});

// Setup event listeners
function setupEventListeners() {
    try {
        if (processBtn) {
            processBtn.addEventListener('click', handleProcess);
        } else {
            console.warn('processBtn not found');
        }
        
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                try {
                    if (userInput) userInput.value = '';
                    if (outputContainer) {
                        outputContainer.innerHTML = '<div class="output-placeholder"><p>Your processed output will appear here...</p></div>';
                    }
                    if (analysisContainer) {
                        analysisContainer.classList.add('analysis-hidden');
                    }
                } catch (e) {
                    console.error('Error in clear handler:', e);
                }
            });
        } else {
            console.warn('clearBtn not found');
        }
        
        if (userInput) {
            userInput.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter') {
                    handleProcess();
                }
            });
        } else {
            console.warn('userInput not found');
        }
        
        // Conversation management event listeners
        if (saveConversationBtn) {
            saveConversationBtn.addEventListener('click', handleSaveConversation);
        }
        if (loadConversationBtn) {
            loadConversationBtn.addEventListener('click', handleLoadConversation);
        }
        if (newConversationBtn) {
            newConversationBtn.addEventListener('click', handleNewConversation);
        }
        if (clearConversationBtn) {
            clearConversationBtn.addEventListener('click', handleClearConversation);
        }
        
        // Footer section toggle listeners
        if (toggleApiEndpointsBtn) {
            toggleApiEndpointsBtn.addEventListener('click', () => toggleFooterSection('api-endpoints'));
        }
        if (toggleActiveSystemsBtn) {
            toggleActiveSystemsBtn.addEventListener('click', () => toggleFooterSection('active-systems'));
        }
        
        // Follow-up button listener
        if (followUpBtn) {
            followUpBtn.addEventListener('click', handleFollowUp);
        }
        if (followUpInput) {
            followUpInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleFollowUp();
                }
            });
        }
    } catch (error) {
        console.error('Error setting up event listeners:', error);
    }
}

// Check server health
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        if (response.ok) {
            const data = await response.json();
            updateStatus('ready', `Ready (${data.systems?.active_systems || 0} systems)`);
            updateAIStatus(!!data.systems?.ai_service && data.systems.ai_service === 'active');
            // Always display the actual model name from the server
            const modelName = data.systems?.ai_model || (data.systems?.ai_service === 'active' ? 'connected' : 'not connected');
            setAIModelLabel(modelName);
            return true;
        } else {
            console.error('Health check failed:', response.status, response.statusText);
            updateStatus('error', `Connection Error (${response.status})`);
            updateAIStatus(false);
            setAIModelLabel('not connected');
            return false;
        }
    } catch (error) {
        console.error('Health check failed:', error);
        updateStatus('error', 'Server not responding - Is the server running?');
        updateAIStatus(false);
        setAIModelLabel('not connected');
        // Retry after 2 seconds
        setTimeout(checkHealth, 2000);
        return false;
    }
}

function setAIModelLabel(modelName) {
    const modelLabel = document.getElementById('ai-service-model-label');
    if (modelLabel) modelLabel.textContent = `AI Service (${modelName})`;
}

// Update AI service status indicator
function updateAIStatus(connected) {
    if (aiStatusLight) {
        if (connected) {
            aiStatusLight.className = 'status-light status-connected';
        } else {
            aiStatusLight.className = 'status-light status-disconnected';
        }
    }
}

// Load system status
async function loadSystemStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/systems`);
        if (response.ok) {
            const data = await response.json();
            if (data.active_systems && data.active_systems.length > 0 && footerSystems) {
                footerSystems.textContent = data.active_systems.join(', ') || 'No systems active';
            }
        }
    } catch (error) {
        console.error('Failed to load system status:', error);
    }
}

// Handle process button click
async function handleProcess() {
    if (!userInput) {
        alert('Input field not found');
        return;
    }
    
    const inputText = userInput.value.trim();
    if (!inputText) {
        alert('Please enter some text to process');
        return;
    }
    
    // Always use AI service (hardcoded to true)
    const useAI = true;
    const level = processingLevel ? processingLevel.value : 'standard';
    
    updateStatus('processing', 'Processing...');
    const startTime = Date.now();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/ethics/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                user_input: inputText,
                processing_level: level,
                use_ai_service: useAI
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        const elapsedTime = Date.now() - startTime;
        
        // Add to conversation history
        conversationHistory.push({
            type: 'user',
            content: inputText,
            timestamp: new Date().toISOString()
        });
        conversationHistory.push({
            type: 'assistant',
            content: data.response,
            timestamp: new Date().toISOString(),
            analysis: data.analysis,
            ethical_score: data.ethical_score,
            status: data.status
        });
        
        // Display output
        displayOutput(data);
        
        // Show follow-up section after first response
        if (followUpSection) {
            followUpSection.style.display = 'block';
        }
        
        // Update status
        updateStatus('ready', 'Complete');
        if (processingTime) {
            processingTime.textContent = `Processing time: ${(elapsedTime / 1000).toFixed(2)}s`;
        }
        
    } catch (error) {
        console.error('Processing error:', error);
        if (outputContainer) {
            outputContainer.innerHTML = `
                <div style="color: #f44336;">
                    <strong>Error:</strong> ${error.message}
                    <br><br>Please check server logs for details.
                </div>
            `;
        }
        updateStatus('error', 'Processing Error');
    }
}

// Display output
function displayOutput(data) {
    try {
        if (!outputContainer) {
            console.error('outputContainer is null');
            return;
        }
        
        // Main response
        const responseText = data.response || 'No response received';
        const formattedText = formatTextWithParagraphs(responseText);
        outputContainer.innerHTML = `
            <div class="output-content">
                ${formattedText}
            </div>
        `;
        
        // Analysis (hidden - keeping code for potential future use)
        if (data.analysis) {
            // Analysis container is kept hidden - do not show
            // if (analysisContainer) {
            //     try {
            //         analysisContainer.classList.remove('analysis-hidden');
            //     } catch (e) {
            //         console.warn('Could not remove analysis-hidden class:', e);
            //     }
            // }
            
            if (analysisContent) {
                try {
                    let analysisHTML = `
                        <div class="analysis-item">
                            <strong>Ethical Score:</strong> ${((data.ethical_score || 0) * 100).toFixed(1)}%
                        </div>
                        <div class="analysis-item">
                            <strong>Status:</strong> ${data.status || 'Unknown'}
                        </div>
                        <div class="analysis-item">
                            <strong>AI Service Used:</strong> ${data.analysis.ai_service_used ? 'Yes' : 'No'}
                        </div>
                    `;
                    
                    if (data.analysis.active_systems && data.analysis.active_systems.length > 0) {
                        analysisHTML += `
                            <div class="analysis-item">
                                <strong>Active Systems:</strong> ${data.analysis.active_systems.length}
                            </div>
                            <div class="systems-badges">
                                ${data.analysis.active_systems.map(s => `<span class="system-badge">${escapeHtml(s)}</span>`).join('')}
                            </div>
                        `;
                    }
                    
                    analysisContent.innerHTML = analysisHTML;
                } catch (e) {
                    console.error('Error setting analysis content:', e);
                }
            }
            
            // Display systems
            if (data.analysis.active_systems && systemsList) {
                try {
                    systemsList.innerHTML = data.analysis.active_systems
                        .map(s => `<div class="system-item">${escapeHtml(s)}</div>`)
                        .join('');
                } catch (e) {
                    console.error('Error setting systems list:', e);
                }
            }
        }
    } catch (error) {
        console.error('Error in displayOutput:', error);
        if (outputContainer) {
            outputContainer.innerHTML = `
                <div style="color: #f44336;">
                    <strong>Error displaying output:</strong> ${error.message}
                </div>
            `;
        }
    }
}

// Update status
function updateStatus(status, text) {
    if (statusText) {
        statusText.textContent = text;
    }
    if (statusIndicator) {
        statusIndicator.className = `status-indicator status-${status}`;
    }
}

// Escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Format text with proper paragraph breaks
function formatTextWithParagraphs(text) {
    if (!text) return '';
    // Escape HTML first
    const escaped = escapeHtml(text);
    // Split by double line breaks (paragraph breaks)
    const paragraphs = escaped.split(/\n\s*\n/);
    // Join with paragraph tags, preserving single line breaks within paragraphs
    return paragraphs.map(para => {
        // Replace single line breaks with <br> within paragraphs
        const formatted = para.replace(/\n/g, '<br>');
        return `<p>${formatted}</p>`;
    }).join('');
}

// Conversation management functions
async function handleSaveConversation() {
    try {
        const name = conversationNameInput ? conversationNameInput.value.trim() : '';
        if (!name) {
            alert('Please enter a conversation name');
            return;
        }
        
        if (conversationHistory.length === 0) {
            alert('No conversation to save');
            return;
        }
        
        const url = currentConversationId 
            ? `${API_BASE_URL}/api/conversations/${currentConversationId}`
            : `${API_BASE_URL}/api/conversations`;
        
        const method = currentConversationId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: name,
                messages: conversationHistory
            })
        });
        
        if (!response.ok) {
            throw new Error(`Failed to save conversation: ${response.status}`);
        }
        
        const data = await response.json();
        if (!currentConversationId) {
            currentConversationId = data.id;
        }
        
        alert('Conversation saved successfully!');
    } catch (error) {
        console.error('Error saving conversation:', error);
        alert(`Error saving conversation: ${error.message}`);
    }
}

async function handleLoadConversation() {
    try {
        // Fetch list of conversations
        // NOTE: Unlimited conversations supported - all conversations are loaded
        const response = await fetch(`${API_BASE_URL}/api/conversations`);
        if (!response.ok) {
            throw new Error('Failed to load conversations list');
        }
        
        const data = await response.json();
        const conversations = data.conversations || [];
        
        if (conversations.length === 0) {
            alert('No saved conversations found');
            return;
        }
        
        // Create a better selection dialog for large numbers of conversations
        // For many conversations, show first 50 in prompt, with option to see more
        const maxDisplayInPrompt = 50;
        let conversationList = '';
        let hasMore = false;
        
        if (conversations.length > maxDisplayInPrompt) {
            // Show first 50
            conversationList = conversations.slice(0, maxDisplayInPrompt).map((conv, index) => 
                `${index + 1}. ${conv.name} (${conv.message_count} messages, updated: ${new Date(conv.updated_at).toLocaleDateString()})`
            ).join('\n');
            hasMore = true;
            conversationList += `\n\n... and ${conversations.length - maxDisplayInPrompt} more conversations.\n\nEnter a number 1-${conversations.length} to select any conversation.`;
        } else {
            // Show all conversations
            conversationList = conversations.map((conv, index) => 
                `${index + 1}. ${conv.name} (${conv.message_count} messages, updated: ${new Date(conv.updated_at).toLocaleDateString()})`
            ).join('\n');
        }
        
        const selection = prompt(`Select a conversation (enter number 1-${conversations.length}):\n\nTotal conversations: ${conversations.length}\n\n${conversationList}`);
        if (!selection) return;
        
        const index = parseInt(selection) - 1;
        if (isNaN(index) || index < 0 || index >= conversations.length) {
            alert(`Invalid selection. Please enter a number between 1 and ${conversations.length}`);
            return;
        }
        
        const selectedConv = conversations[index];
        
        // Load the conversation
        const loadResponse = await fetch(`${API_BASE_URL}/api/conversations/${selectedConv.id}`);
        if (!loadResponse.ok) {
            throw new Error('Failed to load conversation');
        }
        
        const convData = await loadResponse.json();
        
        // Restore conversation
        currentConversationId = convData.id;
        conversationHistory = convData.messages || [];
        
        if (conversationNameInput) {
            conversationNameInput.value = convData.name || '';
        }
        
        // Find and restore the original input (first user message)
        const firstUserMessage = conversationHistory.find(msg => msg.type === 'user');
        if (firstUserMessage && userInput) {
            userInput.value = firstUserMessage.content;
        }
        
        // Display all messages in the output box
        if (outputContainer && conversationHistory.length > 0) {
            let outputHTML = '<div class="output-content">';
            
            // Process all messages in order
            for (let i = 0; i < conversationHistory.length; i++) {
                const msg = conversationHistory[i];
                
                if (msg.type === 'assistant') {
                    // This is a response
                    if (i === 1) {
                        // First response (original)
                        const formattedText = formatTextWithParagraphs(msg.content);
                        outputHTML += `<div>${formattedText}</div>`;
                    } else {
                        // Follow-up response
                        const formattedText = formatTextWithParagraphs(msg.content);
                        outputHTML += `
                            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #ffffff;">
                                <div style="margin-bottom: 10px; color: #ffffff; font-weight: bold;">Follow-up:</div>
                                <div>${formattedText}</div>
                            </div>
                        `;
                    }
                }
            }
            
            outputHTML += '</div>';
            outputContainer.innerHTML = outputHTML;
            
            // Scroll to bottom
            outputContainer.scrollTop = outputContainer.scrollHeight;
        }
        
        // Always show follow-up section when a conversation is loaded
        // This allows users to continue the conversation with follow-up questions
        if (followUpSection) {
            followUpSection.style.display = 'block';
            
            // Populate follow-up conversation display if there are existing follow-ups
            if (followUpConversation) {
                followUpConversation.innerHTML = '';
                
                // Check if there are follow-ups (more than 2 messages = original + response + at least one follow-up)
                if (conversationHistory.length > 2) {
                    // Skip first two messages (original input and first response)
                    for (let i = 2; i < conversationHistory.length; i++) {
                        const msg = conversationHistory[i];
                        const msgDiv = document.createElement('div');
                        
                        if (msg.type === 'user') {
                            msgDiv.className = 'follow-up-message follow-up-question';
                            const formattedText = formatTextWithParagraphs(msg.content);
                            msgDiv.innerHTML = `<strong>You:</strong> ${formattedText}`;
                        } else if (msg.type === 'assistant') {
                            msgDiv.className = 'follow-up-message follow-up-response';
                            const formattedText = formatTextWithParagraphs(msg.content);
                            msgDiv.innerHTML = `<strong>Assistant:</strong> ${formattedText}`;
                        }
                        
                        followUpConversation.appendChild(msgDiv);
                    }
                    
                    followUpConversation.scrollTop = followUpConversation.scrollHeight;
                } else {
                    // No existing follow-ups, but show the section so user can add them
                    followUpConversation.innerHTML = '<div style="color: #ffffff; font-style: italic;">No follow-up questions yet. Ask a follow-up question below to continue the conversation.</div>';
                }
            }
        }
        
        updateStatus('ready', `Loaded: ${convData.name}`);
    } catch (error) {
        console.error('Error loading conversation:', error);
        alert(`Error loading conversation: ${error.message}`);
    }
}

function handleNewConversation() {
    if (confirm('Start a new conversation? Current conversation will be cleared.')) {
        currentConversationId = null;
        conversationHistory = [];
        
        if (conversationNameInput) {
            conversationNameInput.value = '';
        }
        
        if (userInput) {
            userInput.value = '';
        }
        
        if (outputContainer) {
            outputContainer.innerHTML = '<div class="output-placeholder"><p>Your processed output will appear here...</p></div>';
        }
        
        if (analysisContainer) {
            analysisContainer.classList.add('analysis-hidden');
        }
        
        if (followUpSection) {
            followUpSection.style.display = 'none';
        }
        
        if (followUpConversation) {
            followUpConversation.innerHTML = '';
        }
        
        if (followUpInput) {
            followUpInput.value = '';
        }
        
        updateStatus('ready', 'New conversation started');
    }
}

function handleClearConversation() {
    if (confirm('Clear current conversation? This will clear the output and follow-ups, but keep your input text.')) {
        conversationHistory = [];
        
        if (outputContainer) {
            outputContainer.innerHTML = '<div class="output-placeholder"><p>Your processed output will appear here...</p></div>';
        }
        
        if (followUpSection) {
            followUpSection.style.display = 'none';
        }
        
        if (followUpConversation) {
            followUpConversation.innerHTML = '';
        }
        
        if (followUpInput) {
            followUpInput.value = '';
        }
        
        updateStatus('ready', 'Conversation cleared');
    }
}

// Handle follow-up questions
async function handleFollowUp() {
    if (!followUpInput || !userInput) {
        return;
    }
    
    const followUpText = followUpInput.value.trim();
    if (!followUpText) {
        alert('Please enter a follow-up question');
        return;
    }
    
    // Get the original input text
    const originalInput = userInput.value.trim();
    if (!originalInput) {
        alert('No original input found. Please process an input first.');
        return;
    }
    
    // Add follow-up question to conversation display
    if (followUpConversation) {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'follow-up-message follow-up-question';
        const formattedQuestion = formatTextWithParagraphs(followUpText);
        questionDiv.innerHTML = `<strong>You:</strong> ${formattedQuestion}`;
        followUpConversation.appendChild(questionDiv);
        followUpConversation.scrollTop = followUpConversation.scrollHeight;
    }
    
    // Clear the follow-up input
    followUpInput.value = '';
    
    updateStatus('processing', 'Processing follow-up...');
    const startTime = Date.now();
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/ethics/process`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                user_input: originalInput,
                processing_level: processingLevel ? processingLevel.value : 'standard',
                use_ai_service: true,
                follow_up: followUpText
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        const elapsedTime = Date.now() - startTime;
        
        // Add response to conversation display
        if (followUpConversation) {
            const responseDiv = document.createElement('div');
            responseDiv.className = 'follow-up-message follow-up-response';
            const formattedResponse = formatTextWithParagraphs(data.response);
            responseDiv.innerHTML = `<strong>Assistant:</strong> ${formattedResponse}`;
            followUpConversation.appendChild(responseDiv);
            followUpConversation.scrollTop = followUpConversation.scrollHeight;
        }
        
        // Append follow-up response to main output (preserve previous responses)
        if (outputContainer) {
            const existingContent = outputContainer.querySelector('.output-content');
            if (existingContent) {
                // Append to existing content
                const followUpDiv = document.createElement('div');
                followUpDiv.style.marginTop = '20px';
                followUpDiv.style.paddingTop = '20px';
                followUpDiv.style.borderTop = '1px solid #ffffff';
                const formattedText = formatTextWithParagraphs(data.response);
                followUpDiv.innerHTML = `
                    <div style="margin-bottom: 10px; color: #ffffff; font-weight: bold;">Follow-up:</div>
                    <div>${formattedText}</div>
                `;
                existingContent.appendChild(followUpDiv);
            } else {
                // If no existing content, create new
                const formattedText = formatTextWithParagraphs(data.response);
                outputContainer.innerHTML = `
                    <div class="output-content">
                        ${formattedText}
                    </div>
                `;
            }
            // Scroll to bottom to show latest response
            outputContainer.scrollTop = outputContainer.scrollHeight;
        }
        
        // Add to conversation history
        conversationHistory.push({
            type: 'user',
            content: followUpText,
            timestamp: new Date().toISOString()
        });
        conversationHistory.push({
            type: 'assistant',
            content: data.response,
            timestamp: new Date().toISOString(),
            analysis: data.analysis,
            ethical_score: data.ethical_score,
            status: data.status
        });
        
        updateStatus('ready', 'Follow-up complete');
        if (processingTime) {
            processingTime.textContent = `Processing time: ${(elapsedTime / 1000).toFixed(2)}s`;
        }
        
    } catch (error) {
        console.error('Follow-up error:', error);
        if (followUpConversation) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'follow-up-message follow-up-error';
            errorDiv.innerHTML = `<strong>Error:</strong> ${escapeHtml(error.message)}`;
            followUpConversation.appendChild(errorDiv);
        }
        updateStatus('error', 'Follow-up Error');
    }
}

// Toggle footer sections
function toggleFooterSection(sectionName) {
    const contentId = sectionName === 'api-endpoints' ? 'api-endpoints-content' : 'active-systems-content';
    const buttonId = sectionName === 'api-endpoints' ? 'toggle-api-endpoints' : 'toggle-active-systems';
    
    const content = document.getElementById(contentId);
    const button = document.getElementById(buttonId);
    
    if (content && button) {
        const isHidden = content.classList.contains('hidden');
        const icon = button.querySelector('.toggle-icon');
        
        if (isHidden) {
            content.classList.remove('hidden');
            if (icon) icon.textContent = '▼';
        } else {
            content.classList.add('hidden');
            if (icon) icon.textContent = '▶';
        }
    }
}

// Global error handler
window.onerror = function(msg, url, lineNo, columnNo, error) {
    console.error('Global error:', msg, 'at', url, ':', lineNo);
    if (outputContainer) {
        outputContainer.innerHTML = `
            <div style="color: #f44336;">
                <strong>JavaScript Error:</strong> ${msg}
                <br>Please check the browser console for details.
            </div>
        `;
    }
    return false;
};
