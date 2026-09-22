import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Send, Calculator, FileText, User } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import './index.css';

// Using a static user ID for this session
const USER_ID = "local-dev-user-" + Math.floor(Math.random() * 10000);

function App() {
  const [messages, setMessages] = useState([
    { 
      id: 1, 
      text: "Hello! I am your AI Tax Filing Assistant. I can help you analyze your salary structure, figure out the best tax regime, and track what documents you need (like Form 16, Rent Receipts, etc). How can I help you today?", 
      sender: 'bot' 
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: input,
      sender: 'user',
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        message: userMessage.text,
        user_id: USER_ID
      });

      const botMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'bot',
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to connect to the server');
      
      // Remove the loading state, add an error message to the chat
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        text: `Sorry, I encountered an error: ${err.response?.data?.detail || err.message}. Please check if the backend is running and GEMINI_API_KEY is set.`,
        sender: 'bot',
        isError: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-icon">
          <Calculator size={24} />
        </div>
        <div className="header-info">
          <h1>AI Tax Assistant</h1>
          <p>Indian Salaried Employees Guide</p>
        </div>
      </header>

      {error && (
        <div className="error-banner">
          Connection Error: {error}. Make sure the FastAPI backend is running on port 8000.
        </div>
      )}

      <div className="chat-container">
        {messages.map((msg) => (
          <div key={msg.id} className={`message-wrapper ${msg.sender}`}>
            {msg.sender === 'bot' && (
              <div style={{ marginRight: '8px', marginTop: '4px', color: 'var(--primary-color)' }}>
                <Calculator size={20} />
              </div>
            )}
            <div className="message">
              {msg.sender === 'user' ? (
                msg.text
              ) : (
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              )}
            </div>
            {msg.sender === 'user' && (
              <div style={{ marginLeft: '8px', marginTop: '4px', color: 'var(--primary-color)' }}>
                <User size={20} />
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="message-wrapper bot">
            <div style={{ marginRight: '8px', marginTop: '4px', color: 'var(--primary-color)' }}>
              <Calculator size={20} />
            </div>
            <div className="loading-indicator">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <form onSubmit={handleSendMessage} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your tax question here... (e.g. 'I uploaded my Form 16')"
            disabled={isLoading}
          />
          <button type="submit" className="send-button" disabled={!input.trim() || isLoading}>
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
