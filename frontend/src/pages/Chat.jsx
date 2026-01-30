import React, { useState } from "react";
import { sendEmergency } from "../services/api";

export default function Chat() {
  const [message, setMessage] = useState("");
  const [location, setLocation] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!message || !location) return;

    setLoading(true);
    try {
      const data = await sendEmergency(message, location);
      setResult(data);
    } catch (err) {
      alert("Backend error");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", background: "#0b1020", minHeight: "100vh", color: "white" }}>
      <h1>🚨 NeuralForge PS3.23</h1>
      <p>AI Emergency Triage System (SDG 3)</p>

      <textarea
        placeholder="Describe emergency..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{ width: "100%", height: "100px" }}
      />

      <br /><br />

      <input
        placeholder="Location"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        style={{ width: "100%", padding: "10px" }}
      />

      <br /><br />

      <button onClick={handleSend} style={{ padding: "12px 30px", background: "red", color: "white" }}>
        {loading ? "Processing..." : "Send Emergency"}
      </button>

      {result && (
        <div style={{ marginTop: "30px", border: "1px solid cyan", padding: "20px" }}>
          <h3>AI Decision Output</h3>
          <p><b>Category:</b> {result.ai_analysis?.category}</p>
          <p><b>Priority:</b> {result.ai_analysis?.priority}</p>
          <p><b>Authority:</b> {result.authority}</p>
          <p><b>Status:</b> {result.status}</p>
        </div>
      )}
    </div>
  );
}
