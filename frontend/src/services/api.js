import axios from "axios";

/**
 * NeuralForge Backend API
 * Production backend hosted on Render
 */
const API_BASE = "https://neuralforge-backend.onrender.com";

/**
 * Send emergency data to backend AI system
 */
export const sendEmergency = async (message, location) => {
  try {
    const res = await axios.post(`${API_BASE}/api/emergency`, {
      message: message,
      location: location
    });

    return res.data;
  } catch (error) {
    console.error("API ERROR:", error?.response?.data || error.message);
    throw error;
  }
};
