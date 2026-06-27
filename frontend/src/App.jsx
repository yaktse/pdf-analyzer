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

    const [files, setFiles] = useState([
        "book.pdf",
        "notes.pdf"
    ]);

    const [uploadError, setUploadError] = useState("");
    const [uploadStatus, setUploadStatus] = useState("");
    const [statusVisible, setStatusVisible] = useState(false);

    function showUploadStatus(message, isError = false) {
        setUploadError(isError);
        setUploadStatus(message);
        setStatusVisible(true);

        // Start fading after 7 seconds
        setTimeout(() => {
            setStatusVisible(false);
        }, 7000);

        // Remove from DOM after animation completes
        setTimeout(() => {
            setUploadStatus("");
            setUploadError(false);
        }, 8000);
    }

    async function uploadFile(file) {
        const formData = new FormData();

        formData.append("file", file);

        showUploadStatus("Uploading...");

        try {
            await axios.post(
                "http://localhost:8080/upload_pdf",
                formData
            );

            setFiles(prev => [
                ...prev,
                file.name
            ]);

            showUploadStatus(
                `Uploaded: ${file.name}`
            );
        } catch (error) {
            let message = "Upload failed.";

            if (error.response?.data?.detail) {
                message = error.response.data.detail;
            } else if (error.message) {
                message = error.message;
            }

            showUploadStatus(message, true);
        }
    }

    const [sidebarOpen, setSidebarOpen] = useState(true);

    return (
        <div className="app">
            {/* Main content */}

            <div className="main-content">

                {/* Main column */}
                <div className="main-column">
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

                    {/* Input area */}
                    {uploadStatus && (
                        <div
                            className={`upload-status ${
                                uploadError ? "error" : "success"
                            } ${
                                statusVisible ? "visible" : "hidden"
                            }`}
                        >
                            <span>{uploadStatus}</span>

                            <button
                                className="status-close"
                                onClick={() => {
                                    setStatusVisible(false);

                                    setTimeout(() => {
                                        setUploadStatus("");
                                        setUploadError(false);
                                    }, 500);
                                }}
                            >
                                ×
                            </button>
                        </div>
                    )}

                    <div className="input-area">
                        <label className="upload-btn">
                            +
                            <input
                                type="file"
                                accept=".pdf"
                                hidden
                                onChange={(e) => {
                                    const file = e.target.files[0];

                                    if (file) {
                                        uploadFile(file);
                                    }
                                }}
                            />
                        </label>

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

                {/* Side bar area */}
                <div
                    className={`sidebar ${
                        sidebarOpen ? "open" : "closed"
                    }`}
                >
                    <button
                        className="sidebar-toggle"
                        onClick={() =>
                            setSidebarOpen(!sidebarOpen)
                        }
                    >
                        {sidebarOpen ? "→" : "←"}
                    </button>

                    {sidebarOpen && (
                        <div className="sidebar-content">
                            <h3>Corpus</h3>

                            {files.length === 0 ? (
                                <p>No files uploaded.</p>
                            ) : (
                                files.map((file, index) => (
                                    <div
                                        key={index}
                                        className="file-item"
                                    >
                                        📄 {file}
                                    </div>
                                ))
                            )}
                        </div>
                    )}
                </div>
            </div>

        </div>
    );
}

export default App;
