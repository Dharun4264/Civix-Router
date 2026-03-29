# 🏛️ Civix-Router: Smart Governance AI

A working prototype built for the April 3rd Hackathon to bridge the language gap in local governance using Artificial Intelligence.

## 🚀 The Core Problem
Citizens often submit civic complaints in their native regional languages (like Tamil), but government databases and routing systems operate in English. This creates massive delays and misallocated resources. 

## 💡 Our Solution
Civix-Router provides a seamless, dual-portal interface:
1. **Citizen Portal:** Users submit their issues in native Tamil.
2. **Real-Time Translation:** The system instantly translates the context to English.
3. **Zero-Shot AI Classification:** Instead of relying on basic keyword matching, we utilize a highly advanced NLP model (`facebook/bart-large-mnli`) to actually *understand* the complaint and automatically route it to the correct department (Water, Electricity, Public Works, etc.) with a calculated confidence score.
4. **Official Dashboard:** Government workers view an analytics dashboard of categorized, translated issues ready for immediate action.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **AI/ML:** Hugging Face Transformers (PyTorch), Zero-Shot Classification
* **Translation API:** Deep-Translator
* **Data Processing:** Pandas
