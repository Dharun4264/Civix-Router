# 🏛️ Civix-Router: Smart Governance Assistant

A Streamlit app for civic complaint intake and routing, redesigned for accessibility and low-literacy usability.

## 🚀 The Core Problem
Citizens often report civic issues in local languages, while administrative systems and internal workflows are mostly English-first. This slows resolution and can route complaints to the wrong teams.

## 💡 Current Solution
Civix-Router now provides a voice-first and visually guided dual portal:
1. **Citizen Portal (Voice-First Tamil):**
   - Tamil instruction audio playback
   - Microphone-based complaint capture (`st.audio_input`)
   - Text fallback for microphone/network edge cases
   - Clear step cards and large icon-led actions for low-literacy users
2. **Translation + Routing Workflow:**
   - Tamil complaint translated to English via `deep-translator`
   - Complaint routed to department using transparent keyword scoring
   - Progress and confidence feedback shown to the user
3. **Official Dashboard (Interactive):**
   - Department, status, and urgency filters
   - Dynamic KPI cards and charts
   - Triage queue cards for quick prioritization

## 🎨 UX and Accessibility Principles
- Mostly light interface with high readability and clear spacing
- Dark-accent hero sections and red highlight stripes for visual hierarchy
- Strong contrast between text and background for better visibility
- Functional imagery for context (citizen reporting and operations workflow)
- Error handling with retry-friendly guidance

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Translation:** Deep-Translator (`GoogleTranslator`)
- **Voice Prompt Audio:** gTTS
- **Speech-to-Text:** SpeechRecognition (Google recognizer with `ta-IN`)
- **Data and Dashboard:** Pandas

## ▶️ Run Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   streamlit run app.py
   ```

## 📌 Notes
- Speech recognition and translation require network access.
- The current dashboard data is mocked for workflow demonstration and UI testing.
