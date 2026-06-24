import { useState } from "react";
import axios from "axios";
import "./App.css";

// For rendering responses from AI
import ReactMarkdown from "react-markdown";

function App() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    async function sendMessage() {
        if (!input.trim()) return;

        const question = input;

        setMessages(prev => [
            ...prev,
            {
                role: "user",
                text: question
            }
        ]);

        setInput("");
        setLoading(true);

        try {
            const response = await axios.post(
                "http://localhost:8080/chat",
                {
                    question: question
                }
            );

            setMessages(prev => [
                ...prev,
                {
                    role: "assistant",
                    text: response.data.answer
                }
            ]);
        } catch (error) {
            setMessages(prev => [
                ...prev,
                {
                    role: "assistant",
                    text: "Failed to contact server." + error.message
                }
            ]);
        }

        setLoading(false);
    }

    return (
        <div className="app">
            <div className="chat-window">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`message ${msg.role}`}
                    >
                        <div className="bubble">
                            <ReactMarkdown>
                                {msg.text}
                            </ReactMarkdown>
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="message assistant">
                        <div className="bubble">
                            Thinking...
                        </div>
                    </div>
                )}
            </div>

            <div className="input-area">
                <input
                    type="text"
                    value={input}
                    placeholder="Type your message..."
                    onChange={(e) =>
                        setInput(e.target.value)
                    }
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            sendMessage();
                        }
                    }}
                />

                <button onClick={sendMessage}>
                    Send
                </button>
            </div>
        </div>
    );
}

export default App;
