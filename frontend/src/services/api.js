import axios from "axios";

// 🔴 IMPORTANT: This must be your Render backend URL
const API_BASE = "https://neuralforge-backend.onrender.com";

export const sendEmergency = async (message, location) => {
  try {
    const res = await axios.post(`${API_BASE}/api/emergency`, {
      message,
      location
    });

    return res.data; // real backend response
  } catch (err) {
    console.error("API ERROR:", err);
    throw err;
  }
};
