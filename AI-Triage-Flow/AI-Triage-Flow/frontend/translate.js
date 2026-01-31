export const translations = {
    en: {
        title: "REPORT EMERGENCY",
        location: "LOCATION / COORDINATES",
        situation: "SITUATION REPORT",
        initiate: "INITIATE TRIAGE",
        analyzing: "ANALYZING...",
        detect_loc: "DETECT LOCATION",
        listening: "LISTENING...",
        ai_analysis: "AI ANALYSIS",
        severity: "SEVERITY",
        priority: "PRIORITY",
        category: "CATEGORY",
        risk: "RISK ASSESSMENT",
        resources: "REQUIRED RESOURCES",
        routed: "ROUTED AUTHORITY"
    },
    hi: {
        title: "आपातकाल की रिपोर्ट करें",
        location: "स्थान / निर्देशांक",
        situation: "स्थिति रिपोर्ट",
        initiate: "ट्राइएज शुरू करें",
        analyzing: "विश्लेषण कर रहा है...",
        detect_loc: "स्थान का पता लगाएं",
        listening: "सुन रहा हूँ...",
        ai_analysis: "एआई विश्लेषण",
        severity: "तीव्रता",
        priority: "प्राथमिकता",
        category: "श्रेणी",
        risk: "जोखिम मूल्यांकन",
        resources: "आवश्यक संसाधन",
        routed: "अनुप्रेषित प्राधिकरण"
    },
    mr: {
        title: "आणीबाणीची तक्रार करा",
        location: "स्थान / समन्वय",
        situation: "परिस्थिती अहवाल",
        initiate: "ट्राइएज सुरू करा",
        analyzing: "विश्लेषण करत आहे...",
        detect_loc: "स्थान शोधा",
        listening: "ऐकत आहे...",
        ai_analysis: "एआय विश्लेषण",
        severity: "तीव्रता",
        priority: "प्राधान्य",
        category: "श्रेणी",
        risk: "जोखिम मूल्यांकन",
        resources: "आवश्यक संसाधने",
        routed: "राउटेड प्राधिकरण"
    },
    ta: {
        title: "அவசரகால அறிக்கை",
        location: "இடம் / ஒருங்கிணைப்புகள்",
        situation: "சூழ்நிலை அறிக்கை",
        initiate: "பகுப்பாய்வைத் தொடங்கு",
        analyzing: "பகுப்பாய்வு செய்கிறது...",
        detect_loc: "இடத்தைக் கண்டறி",
        listening: "கேட்கிறது...",
        ai_analysis: "AI பகுப்பாய்வு",
        severity: "தீவிரம்",
        priority: "முன்னுரிமை",
        category: "வகை",
        risk: "அபாய மதிப்பீடு",
        resources: "தேவையான வளங்கள்",
        routed: "வழிகாட்டப்பட்ட அதிகாரம்"
    },
    te: {
        title: "అత్యవసర నివేదిక",
        location: "స్థానం / కోఆర్డినేట్లు",
        situation: "పరిస్థితి నివేదిక",
        initiate: "ట్రయేజ్ ప్రారంభించండి",
        analyzing: "విశ్లేషిస్తోంది...",
        detect_loc: "స్థానాన్ని గుర్తించండి",
        listening: "వింటున్నారు...",
        ai_analysis: "AI విశ్లేషణ",
        severity: "తీవ్రత",
        priority: "ప్రాధాన్యత",
        category: "వర్గం",
        risk: "ప్రమాద అంచనా",
        resources: "అవసరమైన వనరులు",
        routed: "రూట్ చేయబడిన అధికారం"
    }
};

export function updateUILanguage(lang) {
    const t = translations[lang] || translations.en;
    document.querySelector('.input-section h2').textContent = t.title;
    document.querySelector('label[for="location"]').textContent = t.location;
    document.querySelector('label[for="message"]').textContent = t.situation;
    document.querySelector('#submitBtn .btn-text').textContent = t.initiate;
    document.querySelector('#detectLocBtn .btn-text').textContent = t.detect_loc;
    document.querySelector('.analysis-header h3').textContent = t.ai_analysis;
    document.querySelector('.severity-card label').textContent = t.severity;
    document.querySelector('.priority-card label').textContent = t.priority;
    document.querySelector('.category-card label').textContent = t.category;
    document.querySelector('.detail-row:nth-child(1) label').textContent = t.risk;
    document.querySelector('.detail-row:nth-child(2) label').textContent = t.resources;
    document.querySelector('.routing-header').textContent = t.routed;
}
