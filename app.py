import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import sklearn
import fastapi

# 1. Setup the Page
st.set_page_config(page_title="Civix-Router Test", page_icon="🏛️")
st.title("🏛️ Civix-Router: Environment Test")
st.write("If you can see this in your browser, your Streamlit frontend is working perfectly!")

# 2. Test the Translator Library
st.subheader("1. Translation API Test")
test_text = st.text_input("Enter Tamil text here to test the translator:", "வணக்கம், இது ஒரு சோதனை")

if st.button("Translate"):
    try:
        # Translating from Tamil ('ta') to English ('en')
        translated = GoogleTranslator(source='ta', target='en').translate(test_text)
        st.success(f"Translation successful: **{translated}**")
    except Exception as e:
        st.error(f"Translation failed. Check your internet or library: {e}")

# 3. Verify ML and Backend Libraries
st.subheader("2. Backend Library Check")
st.info("Checking if your core AI and API libraries are installed correctly...")

st.write(f"✅ Pandas version: `{pd.__version__}`")
st.write(f"✅ Scikit-Learn version: `{sklearn.__version__}`")
st.write(f"✅ FastAPI version: `{fastapi.__version__}`")

st.success("You are ready to build on April 3rd!")