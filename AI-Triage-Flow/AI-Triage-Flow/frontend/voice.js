export function setupVoice(onResult, onStatusChange) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        console.error("Speech recognition not supported in this browser.");
        return null;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US'; // Will be updated by detection or manually if needed

    recognition.onstart = () => onStatusChange(true);
    recognition.onend = () => onStatusChange(false);
    
    recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }
        onResult(finalTranscript || interimTranscript);
    };

    return {
        start: () => recognition.start(),
        stop: () => recognition.stop()
    };
}
