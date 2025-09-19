
import streamlit as st
from dotenv import load_dotenv
import os
from modules.qa_summarizer import QAAndSummarizer
from modules.recommender import Recommender
from modules.finetune import FineTuner
from modules.rag_assistant import RAGAssistant

load_dotenv()
MISTRAL_KEY = os.getenv("MISTRAL_API_KEY", None)

st.set_page_config(page_title="AI Document Intelligence", layout="wide")
st.title("AI-Powered Document/Book Intelligence System (2025)")

tab1, tab2, tab3, tab4 = st.tabs([
    " QA + Summarizer",
    " Recommender",
    " Domain-Specific Fine Tuning",
    " Knowledge Assistant (RAG)"
])

with tab1:
    QAAndSummarizer.render()

with tab2:
    Recommender.render(api_key=MISTRAL_KEY)

with tab3:
    FineTuner.render()

with tab4:
    RAGAssistant.render(api_key=MISTRAL_KEY)
