import { useState } from "react";
import "./ChatBox.css";
import api from "../Services/api";

function ChatBox() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = async () => {
    if (!question.trim()) return;

    // Save user's message
    const userMessage = {
      sender: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await api.post("/chat", null, {
        params: {
          question: question,
        },
      });

      // Save bot reply
      const botMessage = {
        sender: "bot",
        text: response.data.answer,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.log(error);
      const message =
        error.response?.data?.detail ||
        error.message ||
        "Chat request failed";

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: message,
        },
      ]);
    }

    setQuestion("");
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={msg.sender === "user" ? "message user" : "message bot"}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Ask something about your PDF..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default ChatBox;
