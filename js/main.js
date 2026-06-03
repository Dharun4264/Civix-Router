// REPLACE THIS LINK WITH YOUR DEPLOYED GOOGLE SCRIPT URL!
const GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzSCM3tD8DcxdCyfNNDRA_NzcVemmNDxw6Z_lM9LVEUISNJmqRLu44p-K3PYWeOjdYf/exec";

// Animated Counters
const counters = document.querySelectorAll('.counter');
const speed = 200; 

const animateCounters = () => {
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const inc = target / speed;

            if (count < target) {
                counter.innerText = Math.ceil(count + inc);
                setTimeout(updateCount, 15);
            } else {
                counter.innerText = target;
            }
        };
        updateCount();
    });
};

// Trigger counters on scroll
const observer = new IntersectionObserver((entries) => {
    if(entries[0].isIntersecting) {
        animateCounters();
        observer.disconnect();
    }
});
if(counters.length > 0) observer.observe(document.querySelector('.metrics-grid'));

// Voice Recognition Logic (Web Speech API)
function startVoiceRecognition() {
    const micBtn = document.getElementById('micBtn');
    const inputField = document.getElementById('complaintInput');

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        alert("Sorry, your browser doesn't support voice recognition. Please use Chrome.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'ta-IN'; 
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = function() {
        micBtn.style.background = 'rgba(255, 149, 0, 0.2)'; 
        inputField.placeholder = "Listening / கேட்கிறது...";
    };

    recognition.onresult = function(event) {
        const speechResult = event.results[0][0].transcript;
        inputField.value = speechResult;
        micBtn.style.background = 'var(--bg-card)'; 
    };

    recognition.onerror = function(event) {
        console.error("Speech recognition error", event.error);
        micBtn.style.background = 'var(--bg-card)';
        inputField.placeholder = "உதாரணம்: தெரு விளக்கு எரியவில்லை...";
    };

    recognition.onend = function() {
        micBtn.style.background = 'var(--bg-card)';
    };

    recognition.start();
}

// Analytics, Routing & Database Submit
function analyzeAndSubmit() {
    const nameInput = document.getElementById('citizenName').value;
    const phoneInput = document.getElementById('citizenPhone').value;
    const complaintInput = document.getElementById('complaintInput').value;
    const inputLower = complaintInput.toLowerCase();
    const btn = document.getElementById('submitBtn');
    
    // Check if name or complaint are empty
    if(!complaintInput.trim() || !nameInput.trim()) {
        alert("Please enter your name and a complaint to submit.");
        return;
    }

    // STRICT 10-DIGIT PHONE VALIDATION
    const phoneRegex = /^[0-9]{10}$/;
    if(!phoneRegex.test(phoneInput)) {
        alert("Please enter exactly 10 numbers for your phone number.");
        return;
    }


    // UI Loading State
    btn.innerText = "Routing & Saving...";
    btn.style.opacity = "0.7";

    let translation = "Street light is not working / Power issue detected";
    let department = "General Administration";

    // Routing Logic matching project spec
    if (inputLower.includes('water') || inputLower.includes('pipe') || inputLower.includes('leak') || inputLower.includes('drinking') || inputLower.includes('தண்ணீர்') || inputLower.includes('குழாய்')) {
        translation = "Water pipe leak / Drinking water supply disruption reported";
        department = "Water Supply Department";
    } else if (inputLower.includes('light') || inputLower.includes('electricity') || inputLower.includes('power') || inputLower.includes('wire') || inputLower.includes('விளக்கு') || inputLower.includes('மின்சாரம்')) {
        translation = "Street light failure / Electrical power wire hazard";
        department = "Electricity Board";
    } else if (inputLower.includes('road') || inputLower.includes('pothole') || inputLower.includes('street') || inputLower.includes('damage') || inputLower.includes('சாலை') || inputLower.includes('பள்ளம்')) {
        translation = "Road damage and potholes causing traffic risk";
        department = "Public Works Department";
    } else {
        translation = complaintInput; 
    }

    // Package data for Google Sheets
    const formData = new URLSearchParams();
    formData.append("name", nameInput);
    formData.append("phone", phoneInput);
    formData.append("complaint", complaintInput);
    formData.append("translation", translation);
    formData.append("department", department);

    // Send to Google Sheets API
    fetch(GOOGLE_SCRIPT_URL, {
        method: 'POST',
        body: formData,
        mode: 'no-cors' 
    })
    .then(() => {
        // Show success UI
        document.getElementById('demoResult').style.display = 'block';
        document.getElementById('translatedText').innerText = `"${translation}"`;
        document.getElementById('routedDept').innerText = `⚙️ ${department} (Saved to DB ✅)`;
        
        // Reset button
        btn.innerText = "Submit to Database";
        btn.style.opacity = "1";
    })
    .catch(error => {
        console.error('Error!', error.message);
        btn.innerText = "Submit to Database";
        btn.style.opacity = "1";
        alert("Failed to save to database. Please check console.");
    });
}