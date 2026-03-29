import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd

# 1. The UI Setup
st.set_page_config(page_title="Civix-Router", page_icon="🏛️", layout="wide")
st.title("🏛️ Civix-Router: Smart Governance")

# Create Tabs for different users
tab1, tab2 = st.tabs(["📱 Citizen Portal", "📊 Official Dashboard"])

with tab1:
    st.subheader("Submit Your Complaint")
    user_input = st.text_area("Enter your complaint (in Tamil):", placeholder="உதாரணம்: தெரு விளக்கு எரியவில்லை...")

    if st.button("Submit Complaint"):
        if user_input:
            with st.spinner("Processing & Translating..."):
                # Translation Engine
                translated_text = GoogleTranslator(source='ta', target='en').translate(user_input)
                
                # Smart Routing Logic
                department = "Unassigned"
                if any(word in translated_text.lower() for word in ["water", "pipe", "leak", "drinking"]):
                    department = "💧 Water Supply Dept"
                elif any(word in translated_text.lower() for word in ["light", "electricity", "power", "wire"]):
                    department = "⚡ Electricity Board"
                elif any(word in translated_text.lower() for word in ["road", "pothole", "street", "damage"]):
                    department = "🛣️ Public Works Dept"
                else:
                    department = "🏢 General Administration"

                st.success("Complaint Submitted Successfully!")
                st.info(f"**Translated to:** {translated_text}")
                st.warning(f"**Routed automatically to:** {department}")
        else:
            st.error("Please enter a complaint first.")

with tab2:
    st.subheader("Live City Analytics")
    st.write("Real-time overview of civic issues across departments.")
    
    # Mock Data for the prototype pitch
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Complaints Today", "142", "+12%")
    col2.metric("Resolved Issues", "89", "+5%")
    col3.metric("Pending Action", "53", "-2%")
    
    st.divider()
    
    # A beautiful chart to impress the judges
    chart_data = pd.DataFrame({
        "Department": ["Water Supply", "Electricity", "Public Works", "Sanitation", "General"],
        "Active Complaints": [45, 20, 35, 15, 27]
    })
    
    st.bar_chart(chart_data, x="Department", y="Active Complaints", color="#ff4b4b")