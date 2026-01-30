import axios from "axios";

const API_BASE = "https://neuralforge-backend.onrender.com";

export const sendEmergency = async (message, location) => {
  const res = await axios.post(`${API_BASE}/api/emergency`, {
    message,
    location
  });
  return res.data;
};
