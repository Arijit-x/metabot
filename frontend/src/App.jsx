import React, { useState, useRef, useEffect } from "react";
import "./App.css";

const BACKEND_URL = "http://127.0.0.1:8000";

const SUGGESTIONS = [
  "Which tables contain customer data?",
  "Who owns the orders table?",
  "Show me recently updated tables",
  "What columns does the users table have?",
  "Show lineage for the revenue table",
  "Which tables have PII tags?",
];

function TypingIndicator() {
  return (
    <div className="message bot-message">
      <div className="avatar bot-avatar">🤖</div>
      <div className="bubble typing-bubble">
        <span className="dot" /><span className="dot" /><span className="dot" />
      </div>
    </div>
  );
}

function Message({ msg }) {
  const isUser = msg.role === "user";
  return (
    <div className={`message ${isUser ? "user-message" : "bot-message"}`}>
      {!isUser && <div className="avatar bot-avatar">🤖</div>}
      <div className={`bubble ${isUser ? "user-bubble" : "bot-bubble"}`}>
        <pre className="message-text">{msg.text}</pre>
        <span className="timestamp">{msg.time}</span>
      </div>
      {isUser && <div className="avatar user-avatar">👤</div>}
    </div>
  );
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "bot",
      text: "👋 Hi! I'm MetaBot, your AI-powered data catalog assistant.\n\nI can help you:\n• 🔍 Search and discover tables\n• 👤 Find table owners\n• 📋 Explore columns and schemas\n• 🔗 Trace data lineage\n• 🏷️ Find tagged datasets\n\nTry asking me something below!",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async (text) => {
    const question = text || input.trim();
    if (!question || loading) return;

    const time = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    const userMsg = { role: "user", text: question, time };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: question, history }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();

      const botMsg = {
        role: "bot",
        text: data.response,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      };
      setMessages((prev) => [...prev, botMsg]);
      setHistory((prev) => [
        ...prev,
        { role: "user", text: question },
        { role: "model", text: data.response },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: `⚠️ Error: ${err.message}\n\nMake sure the backend is running at ${BACKEND_URL}`,
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const clearChat = () => {
    setMessages([{
      role: "bot",
      text: "Chat cleared! Ask me anything about your data catalog.",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    }]);
    setHistory([]);
  };

  return (
    <div className="app">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <span className="logo-icon">🤖</span>
          <div>
            <div className="logo-title">MetaBot</div>
            <div className="logo-sub">Data Catalog Assistant</div>
          </div>
        </div>

        <div className="sidebar-section">
          <div className="sidebar-label">💡 Try asking</div>
          {SUGGESTIONS.map((s, i) => (
            <button key={i} className="suggestion-btn" onClick={() => sendMessage(s)}>
              {s}
            </button>
          ))}
        </div>

        <div className="sidebar-section">
          <div className="sidebar-label">⚡ Powered by</div>
          <div className="powered-by">
            <div className="powered-item">🧠  Groq LLaMA 3.3</div>
            <div className="powered-item">📊 OpenMetadata</div>
            <div className="powered-item">⚡ FastAPI</div>
          </div>
        </div>

        <button className="clear-btn" onClick={clearChat}>🗑️ Clear Chat</button>
      </aside>

      {/* Main Chat */}
      <main className="chat-area">
        <header className="chat-header">
          <div className="header-info">
            <div className="header-title">MetaBot</div>
            <div className="header-status">
              <span className="status-dot" />
              AI-powered data discovery
            </div>
          </div>
        </header>

        <div className="messages-container">
          {messages.map((msg, i) => <Message key={i} msg={msg} />)}
          {loading && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>

        <div className="input-area">
          <input
            ref={inputRef}
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
            placeholder="Ask about your data catalog... (e.g. Who owns the orders table?)"
            disabled={loading}
          />
          <button
            className="send-btn"
            onClick={() => sendMessage()}
            disabled={loading || !input.trim()}
          >
            {loading ? "⏳" : "➤"}
          </button>
        </div>
      </main>
    </div>
  );
}
