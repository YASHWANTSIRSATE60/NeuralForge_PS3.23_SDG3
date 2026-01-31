import { setupVoice } from './voice.js';
import { getLocation } from './location.js';
import { updateUILanguage } from './translate.js';

let voiceEngine = null;

document.addEventListener('DOMContentLoaded', () => {
    // Initialize components
    initLanguage();
    initLocation();
    initVoice();
    initNetwork();
    
    // Form handling
    document.getElementById('emergencyForm').addEventListener('submit', handleTriage);
});

function initLanguage() {
    const langSelect = document.getElementById('langSelect');
    langSelect.addEventListener('change', (e) => {
        updateUILanguage(e.target.value);
    });
}

function initLocation() {
    const detectBtn = document.getElementById('detectLocBtn');
    const locInput = document.getElementById('location');
    const locAcc = document.getElementById('locAccuracy');

    detectBtn.addEventListener('click', () => {
        locInput.placeholder = "Locating...";
        getLocation(
            (data) => {
                locInput.value = data.address;
                locAcc.textContent = `±${Math.round(data.accuracy)}m`;
            },
            (err) => {
                locInput.placeholder = "Detection failed. Enter manually.";
                console.error(err);
            }
        );
    });
}

function initVoice() {
    const micBtn = document.getElementById('micBtn');
    const messageArea = document.getElementById('message');
    const statusText = document.getElementById('voiceStatus');

    voiceEngine = setupVoice(
        (text) => {
            messageArea.value = text;
        },
        (isListening) => {
            micBtn.classList.toggle('active', isListening);
            statusText.classList.toggle('hidden', !isListening);
        }
    );

    if (voiceEngine) {
        micBtn.addEventListener('click', () => {
            if (micBtn.classList.contains('active')) {
                voiceEngine.stop();
            } else {
                voiceEngine.start();
            }
        });
    } else {
        micBtn.style.display = 'none';
    }
}

function initNetwork() {
    const banner = document.getElementById('offline-banner');
    const status = document.getElementById('netStatus');
    
    window.addEventListener('online', () => {
        banner.classList.add('hidden');
        status.textContent = "SYSTEM ONLINE";
        status.style.color = "var(--success-color)";
    });
    
    window.addEventListener('offline', () => {
        banner.classList.remove('hidden');
        status.textContent = "SYSTEM OFFLINE";
        status.style.color = "var(--alert-color)";
    });
}

async function handleTriage(e) {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const loader = document.getElementById('loader');
    const btnText = submitBtn.querySelector('.btn-text');
    const outputSection = document.getElementById('outputSection');
    
    if (navigator.onLine === false) {
        alert("CRITICAL: Network connection required for AI analysis.");
        return;
    }

    submitBtn.disabled = true;
    loader.style.display = 'block';
    const originalText = btnText.textContent;
    btnText.textContent = 'ANALYZING...';
    
    const payload = {
        message: document.getElementById('message').value,
        location: document.getElementById('location').value,
        lang: document.getElementById('langSelect').value
    };

    try {
        const response = await fetch('/api/emergency', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
        
        const data = await response.json();
        renderResult(data);
    } catch (err) {
        console.error(err);
        alert("SYSTEM ERROR: Failed to communicate with Core AI.");
    } finally {
        submitBtn.disabled = false;
        loader.style.display = 'none';
        btnText.textContent = originalText;
    }
}

function renderResult(data) {
    const output = document.getElementById('outputSection');
    output.classList.remove('hidden');
    
    document.getElementById('severityVal').textContent = data.severity;
    document.getElementById('priorityVal').textContent = data.priority;
    document.getElementById('categoryVal').textContent = data.category;
    document.getElementById('riskVal').textContent = data.risk;
    document.getElementById('helpVal').textContent = data.required_help;
    document.getElementById('detectedLang').textContent = `LANG: ${data.detected_language || '--'}`;
    document.getElementById('confScore').textContent = `CONF: ${Math.round((data.confidence_score || 0.9) * 100)}%`;
    document.getElementById('timestamp').textContent = new Date().toLocaleTimeString();

    const routing = data.routing_info;
    document.getElementById('routingUnit').textContent = routing.unit;
    document.getElementById('routingCode').textContent = routing.code;
    document.getElementById('routingDesc').textContent = routing.description;

    output.scrollIntoView({ behavior: 'smooth' });
}
