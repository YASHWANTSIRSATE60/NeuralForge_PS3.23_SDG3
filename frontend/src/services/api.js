import axios from "axios";

// For local development run backend at http://localhost:8000
// When deployed, set this to the backend host (e.g. https://neuralforge-backend.onrender.com)
// Use environment variable REACT_APP_API_BASE or fall back to localhost for dev
const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";

export const sendEmergency = async (message, location) => {
  const res = await axios.post(`${API_BASE}/api/emergency`, {
    message,
    location
  });
  return res.data;
};
