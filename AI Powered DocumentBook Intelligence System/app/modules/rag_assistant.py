
import streamlit as st
import tempfile, os
from modules.loaders import load_pdf_to_docs, split_documents
from modules.embeddings_store import get_embeddings, load_or_create_chroma
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
# Optional: Chat Mistral interface wrapper
try:
    from langchain_mistralai import ChatMistralAI
except Exception:
    ChatMistralAI = None

PERSIST_DIR = "chroma_db"

class RAGAssistant:
    @staticmethod
    def render(api_key=None):
        st.header("Knowledge Assistant (RAG-based)")
        st.info("Stores book data permanently in a Chroma DB for retrieval anytime.")

        embeddings = get_embeddings()
        vectorstore = None

        # Load existing Chroma DB if available
        if os.path.exists(PERSIST_DIR):
            try:
                vectorstore = load_or_create_chroma(PERSIST_DIR, embeddings=embeddings)
            except Exception as e:
                st.warning(f"Could not load existing Chroma DB: {e}")

        uploaded_files = st.file_uploader(
            "Upload one or more PDF files (they will be saved permanently)",
            type="pdf",
            accept_multiple_files=True
        )

        if uploaded_files:
            documents = []
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name

                docs = load_pdf_to_docs(tmp_path)
                documents.extend(docs)

            if documents:
                st.success(f"✅ Processed {len(uploaded_files)} new file(s). Adding to knowledge base...")
                splits = split_documents(documents, chunk_size=1000, chunk_overlap=200)

                if vectorstore:
                    vectorstore.add_documents(splits)
                else:
                    vectorstore = load_or_create_chroma(PERSIST_DIR, docs=splits, embeddings=embeddings)

                try:
                    vectorstore.persist()
                    st.success("📂 Knowledge base updated and saved!")
                except Exception as e:
                    st.error(f"Failed to persist vectorstore: {e}")

        if vectorstore:
            retriever = vectorstore.as_retriever()
            memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

            if ChatMistralAI is None:
                st.warning("ChatMistralAI wrapper not installed — conversational LLM will not be available.")
                st.info("You can still query the retriever and inspect top docs programmatically.")

            else:
                llm = ChatMistralAI(
                    api_key=api_key,
                    model="mistral-small-latest",
                    temperature=0.2,
                    base_url="https://api.mistral.ai/v1"
                )

                qa_chain = ConversationalRetrievalChain.from_llm(
                    llm=llm,
                    retriever=retriever,
                    memory=memory
                )

                st.subheader("💬 Ask me anything about your books")
                if "history" not in st.session_state:
                    st.session_state["history"] = []

                query = st.text_input("Enter your question:", key="rag_query")
                if query:
                    with st.spinner("Thinking..."):
                        response = qa_chain.run(query)
                    st.session_state["history"].append((query, response))

                for user_q, bot_a in st.session_state["history"]:
                    st.markdown(f"**You:** {user_q}")
                    st.markdown(f"**Assistant:** {bot_a}")
        else:
            st.info("📂 Upload some PDFs to build your knowledge base.")
