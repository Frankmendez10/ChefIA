import { useState } from "react";
import "./App.css";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const API_URL = "http://127.0.0.1:8000/api/assistant/chat";

function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    const text = message.trim();

    if (!text || loading) return;

    setMessages((current) => [
      ...current,
      { role: "user", content: text },
    ]);

    setMessage("");
    setLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: text }),
      });

      if (!response.ok) {
        throw new Error("Error en la API");
      }

      const data = await response.json();

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            "No pude conectarme con ChefIA. Verifica que el backend esté funcionando.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (
    event: React.KeyboardEvent<HTMLTextAreaElement>
  ) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>🍳 ChefIA</h1>
          <p>Tu asistente culinario inteligente</p>
        </div>
      </header>

      <main className="chat-container">
        {messages.length === 0 ? (
          <div className="welcome">
            <div className="welcome-icon">👨‍🍳</div>

            <h2>¿Qué quieres cocinar hoy?</h2>

            <p>
              Pregúntame por recetas, sustituciones, tiempos de
              cocción o recomendaciones.
            </p>

            <div className="examples">
              <button
                onClick={() =>
                  setMessage(
                    "Tengo pollo y arroz, ¿qué puedo preparar?"
                  )
                }
              >
                🍗 Receta con pollo y arroz
              </button>

              <button
                onClick={() =>
                  setMessage(
                    "¿Con qué puedo sustituir la leche?"
                  )
                }
              >
                🥛 Sustituir la leche
              </button>

              <button
                onClick={() =>
                  setMessage(
                    "Quiero una cena rápida y saludable."
                  )
                }
              >
                🥗 Cena rápida y saludable
              </button>
            </div>
          </div>
        ) : (
          <div className="messages">
            {messages.map((item, index) => (
              <div
                key={index}
                className={`message ${
                  item.role === "user"
                    ? "user-message"
                    : "assistant-message"
                }`}
              >
                <div className="message-label">
                  {item.role === "user" ? "Tú" : "ChefIA"}
                </div>

                <div className="message-content">
                  {item.content}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message assistant-message">
                <div className="message-label">ChefIA</div>
                <div className="message-content loading">
                  ChefIA está pensando...
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <div className="input-area">
        <textarea
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Escribe lo que quieres cocinar..."
          rows={2}
          disabled={loading}
        />

        <button
          className="send-button"
          onClick={sendMessage}
          disabled={!message.trim() || loading}
        >
          {loading ? "..." : "Enviar"}
        </button>

        <small>
          Enter para enviar · Shift + Enter para nueva línea
        </small>
      </div>
    </div>
  );
}

export default App;