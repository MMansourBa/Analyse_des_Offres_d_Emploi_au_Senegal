import { useState } from "react";
import { sendChat } from "../services/api";

const SUGGESTIONS = [
  "Quel secteur recrute le plus ?",
  "Quelles compétences sont demandées à Dakar ?",
  "Combien d'offres CDI ce mois-ci ?",
  "Quelle ville offre le plus d'opportunités en IT ?",
];

export default function Assistant() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const envoyer = async (msg) => {
    const question = msg || input;
    if (!question.trim()) return;
    setMessages(m => [...m, { role: "user", text: question }]);
    setInput("");
    setLoading(true);
    try {
      const r = await sendChat(question);
      setMessages(m => [...m, { role: "assistant", text: r.data.response }]);
    } catch {
      setMessages(m => [...m, { role: "assistant", text: "Erreur de connexion." }]);
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", background: "#0D0D2B", minHeight: "100vh", color: "white" }}>
      <h1 style={{ color: "#F5A623" }}>Assistant IA</h1>

      {/* Suggestions */}
      <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "1rem" }}>
        {SUGGESTIONS.map((s, i) => (
          <button key={i} onClick={() => envoyer(s)}
            style={{ padding: "0.5rem 1rem", background: "#1A1A3E", color: "#F5A623",
              border: "1px solid #F5A623", borderRadius: "20px", cursor: "pointer" }}>
            {s}
          </button>
        ))}
      </div>

      {/* Messages */}
      <div style={{ background: "#1A1A3E", borderRadius: "8px", padding: "1rem",
        height: "400px", overflowY: "auto", marginBottom: "1rem" }}>
        {messages.map((m, i) => (
          <div key={i} style={{
            textAlign: m.role === "user" ? "right" : "left",
            marginBottom: "1rem"
          }}>
            <span style={{
              background: m.role === "user" ? "#6C3FC5" : "#2C2C5E",
              padding: "0.75rem 1rem", borderRadius: "12px", display: "inline-block",
              maxWidth: "70%"
            }}>
              {m.text}
            </span>
          </div>
        ))}
        {loading && <p style={{ color: "#aaa" }}>En train de répondre...</p>}
      </div>

      {/* Input */}
      <div style={{ display: "flex", gap: "0.5rem" }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && envoyer()}
          placeholder="Posez votre question..."
          style={{ flex: 1, padding: "0.75rem", borderRadius: "4px",
            border: "1px solid #F5A623", background: "#1A1A3E", color: "white" }}
        />
        <button onClick={() => envoyer()}
          style={{ padding: "0.75rem 1.5rem", background: "#F5A623", color: "#0D0D2B",
            border: "none", borderRadius: "4px", cursor: "pointer", fontWeight: "bold" }}>
          Envoyer
        </button>
      </div>
    </div>
  );
}