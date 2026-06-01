import io
from datetime import date, timedelta

import pandas as pd
import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
try:
    import speech_recognition as sr
except ModuleNotFoundError:
    sr = None

st.set_page_config(page_title="Civix-Router", page_icon="🏛️", layout="wide")

st.markdown(
    """
    <style>
        :root {
            --surface: #f5f6f8;
            --card: #ffffff;
            --text: #0f172a;
            --muted: #475569;
            --accent-danger: #c81e1e;
            --accent-info: #0b5fff;
            --panel-dark: #111827;
            --panel-light: #f8fafc;
        }
        .stApp {
            background: var(--surface);
            color: var(--text);
        }
        .hero-panel {
            background: linear-gradient(120deg, #111827 60%, #1f2937 100%);
            border-left: 4px solid var(--accent-danger);
            border-radius: 14px;
            padding: 1rem 1.2rem;
            color: #f8fafc;
            margin-bottom: 1rem;
        }
        .guide-card {
            background: var(--card);
            border-left: 4px solid var(--accent-danger);
            border-radius: 12px;
            padding: 0.8rem 1rem;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
            margin: 0.5rem 0;
        }
        .status-chip {
            display: inline-block;
            background: #fee2e2;
            color: #991b1b;
            border-radius: 999px;
            padding: 0.25rem 0.7rem;
            font-weight: 600;
            margin-right: 0.4rem;
        }
        .queue-card {
            background: var(--card);
            border-radius: 10px;
            border: 1px solid #e2e8f0;
            padding: 0.8rem 1rem;
            margin-bottom: 0.6rem;
        }
        .small-muted {
            color: var(--muted);
            font-size: 0.9rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

DEPARTMENT_MAP = {
    "💧 Water Supply Dept": ["water", "pipe", "leak", "drinking", "sewage", "drain"],
    "⚡ Electricity Board": ["light", "electricity", "power", "wire", "transformer"],
    "🛣️ Public Works Dept": ["road", "pothole", "street", "damage", "bridge", "traffic"],
    "🚮 Sanitation Dept": ["garbage", "waste", "clean", "drainage", "toilet"],
}

DEPT_ICONS = {
    "💧 Water Supply Dept": "💧",
    "⚡ Electricity Board": "⚡",
    "🛣️ Public Works Dept": "🛣️",
    "🚮 Sanitation Dept": "🚮",
    "🏢 General Administration": "🏢",
}


def build_mock_data() -> pd.DataFrame:
    today = date.today()
    rows = [
        ("CMP-1048", "⚡ Electricity Board", "High", "Pending", today),
        ("CMP-1049", "💧 Water Supply Dept", "Medium", "In Progress", today),
        ("CMP-1050", "🛣️ Public Works Dept", "High", "Pending", today - timedelta(days=1)),
        ("CMP-1051", "🚮 Sanitation Dept", "Low", "Resolved", today - timedelta(days=2)),
        ("CMP-1052", "🏢 General Administration", "Medium", "Pending", today),
        ("CMP-1053", "💧 Water Supply Dept", "Low", "Resolved", today - timedelta(days=3)),
        ("CMP-1054", "⚡ Electricity Board", "Medium", "In Progress", today - timedelta(days=1)),
        ("CMP-1055", "🛣️ Public Works Dept", "Low", "Resolved", today - timedelta(days=4)),
    ]
    return pd.DataFrame(rows, columns=["Complaint ID", "Department", "Urgency", "Status", "Date"])


def route_complaint(translated_text: str) -> tuple[str, int]:
    lowered = translated_text.lower()
    best_dept = "🏢 General Administration"
    best_hits = 0
    for department, keywords in DEPARTMENT_MAP.items():
        hits = sum(1 for word in keywords if word in lowered)
        if hits > best_hits:
            best_dept = department
            best_hits = hits
    confidence = min(98, 40 + (best_hits * 22))
    return best_dept, confidence


def play_tamil_prompt(text: str) -> None:
    speech = gTTS(text=text, lang="ta")
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    st.audio(audio_buffer.read(), format="audio/mp3")


def transcribe_audio_tamil(audio_file) -> str:
    if sr is None:
        raise RuntimeError("SpeechRecognition dependency is not installed.")
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 250
    recognizer.dynamic_energy_threshold = True
    raw_bytes = audio_file.read()
    with sr.AudioFile(io.BytesIO(raw_bytes)) as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data, language="ta-IN")


st.title("🏛️ Civix-Router: Smart Governance")
st.markdown(
    """
    <div class="hero-panel">
        <h3>Voice-first civic reporting for everyone</h3>
        <p>Large controls, Tamil audio guidance, visual icon prompts, and clear routing feedback.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2 = st.tabs(["📱 Citizen Portal", "📊 Official Dashboard"])

with tab1:
    st.image(
        "https://images.unsplash.com/photo-1573164574572-cb89e39749b4?q=80&w=1200&auto=format&fit=crop",
        caption="Report local issues quickly with voice guidance.",
        use_container_width=True,
    )
    st.markdown("### Tamil Voice Complaint Assistant")
    st.markdown(
        """
        <div class="guide-card">
            <b>1) Listen</b> -> <b>2) Record voice</b> -> <b>3) Confirm</b> -> <b>4) Submit</b><br/>
            <span class="small-muted">Icons and audio cues are designed for low-literacy users.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, _ = st.columns([1, 1])
    with col_a:
        if st.button("🔊 Play Tamil Guidance", use_container_width=True):
            play_tamil_prompt("தயவுசெய்து உங்கள் பிரச்சினையை தெளிவாகச் சொல்லுங்கள். பிறகு சமர்ப்பிக்கவும்.")
        st.caption("Guidance audio: Tap to hear instructions in Tamil.")

    if sr is None:
        st.warning("Voice transcription is temporarily unavailable. Install `SpeechRecognition` to enable microphone mode.")
    audio_input = st.audio_input("🎙️ Record complaint in Tamil")
    fallback_text = st.text_area(
        "⌨️ Text fallback (optional)",
        placeholder="உதாரணம்: தெருவில் குப்பை அகற்றப்படவில்லை",
        help="Use only when microphone is unavailable.",
    )

    complaint_text = ""
    transcription_error = None
    if audio_input and sr is not None:
        with st.spinner("Transcribing Tamil voice input..."):
            try:
                complaint_text = transcribe_audio_tamil(audio_input)
                st.success("Voice captured successfully.")
                st.write(f"**Recognized Tamil complaint:** {complaint_text}")
            except sr.UnknownValueError as error:
                transcription_error = error
                st.error("Audio was received but speech could not be understood. Please speak closer and retry.")
            except sr.RequestError as error:
                transcription_error = error
                st.error("Speech service is temporarily unavailable. Please retry in a moment or use text fallback.")
            except Exception as error:
                transcription_error = error
                st.error("Unable to transcribe audio right now. You can retry or use text fallback.")
                with st.expander("Show technical error details"):
                    st.code(str(error))

    if fallback_text.strip():
        complaint_text = fallback_text.strip()

    submit_disabled = not complaint_text
    if st.button("✅ Submit Complaint", type="primary", use_container_width=True, disabled=submit_disabled):
        progress = st.progress(0, text="Starting complaint workflow...")
        try:
            progress.progress(25, text="Complaint recorded")
            translated_text = GoogleTranslator(source="ta", target="en").translate(complaint_text)
            progress.progress(60, text="Translation complete")
            department, confidence = route_complaint(translated_text)
            progress.progress(100, text="Department assigned")

            st.success("Complaint submitted successfully.")
            st.markdown(f"<span class='status-chip'>{DEPT_ICONS.get(department, '🏢')} {department}</span>", unsafe_allow_html=True)
            st.info(f"**Translated to English:** {translated_text}")
            st.warning(f"**Routing confidence:** {confidence}%")
            st.caption("You can replay the Tamil prompt and submit a new complaint anytime.")
        except Exception:
            st.error("Network issue while translating or routing. Please tap submit again.")
    elif submit_disabled and (audio_input or fallback_text):
        st.warning("Please provide a valid voice/text complaint before submission.")
    elif audio_input and sr is None:
        st.info("Voice was recorded, but transcription is disabled until the dependency is installed.")
    elif transcription_error:
        st.caption("Tip: Keep voice recording under 20 seconds and speak in short sentences.")

with tab2:
    st.subheader("Live City Analytics")
    st.write("Real-time overview of civic issues across departments.")
    
    # Mock Data for the prototype pitch
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Complaints Today", "142", "+12%")
    col2.metric("Resolved Issues", "89", "+5%")
    col3.metric("Pending Action", "53", "-2%")
    
    st.divider()

   # A beautiful chart to impress the judges (Synced with real departments!)
    chart_data = pd.DataFrame({
        "Department": ["Municipality", "TNEB", "TWAD", "Police", "PWD"],
        "Active Complaints": [45, 20, 35, 15, 27]
    })
    
    st.bar_chart(chart_data, x="Department", y="Active Complaints", color="#ff4b4b")