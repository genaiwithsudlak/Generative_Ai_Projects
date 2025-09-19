
import streamlit as st
import tempfile
from modules.loaders import load_pdf_to_docs, split_documents
from modules.embeddings_store import get_embeddings, create_faiss_from_docs
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.chains import RetrievalQA

class QAAndSummarizer:
    @staticmethod
    def render():
        st.header(" QA + Summarizer")
        st.info("One-time use only, does not store data. Upload a PDF to ask questions or generate summaries.")
        uploaded_file = st.file_uploader("Upload PDF", type="pdf", key="qa_summarizer")
        if not uploaded_file:
            return

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        documents = load_pdf_to_docs(tmp_path)
        docs = split_documents(documents, chunk_size=400, chunk_overlap=50)

        embeddings = get_embeddings()
        db = create_faiss_from_docs(docs, embeddings)

        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

        qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base", max_length=256)
        llm = HuggingFacePipeline(pipeline=qa_pipeline)
        qa = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

        tab1a, tab1b = st.tabs(["💬 Ask Questions", "📝 Summarize"])
        with tab1a:
            query = st.text_input("Ask a question about the PDF:")
            if query:
                response = qa.run(query)
                st.write("**Answer:**", response)

        with tab1b:
            if st.button("Summarize PDF"):
                full_text = " ".join([doc.page_content for doc in docs])
                chunks = [full_text[i:i+800] for i in range(0, len(full_text), 800)]
                summaries = [
                    summarizer(chunk, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
                    for chunk in chunks
                ]
                st.subheader("📑 PDF Summary")
                st.write(" ".join(summaries))
