
import streamlit as st
from mistralai import Mistral

class Recommender:
    @staticmethod
    def render(api_key=None):
        st.header("Book / Document Recommender")
        st.info("Get personalized book/document recommendations.")
        book_name = st.text_input("Enter a book name:")
        if book_name and api_key:
            st.write(f"🔍 Finding books similar to: **{book_name}**")
            prompt = f"Recommend 5 books that are similar to '{book_name}'. Return them as a numbered list with title and author."
            client = Mistral(api_key=api_key)
            with st.spinner("Fetching recommendations..."):
                response = client.chat.complete(
                    model="mistral-small-latest",
                    messages=[{"role": "user", "content": prompt}]
                )
                recs = response.choices[0].message.content
            st.subheader("📖 Recommended Books")
            st.write(recs)
        elif book_name and not api_key:
            st.warning("No API key found. Put MISTRAL_API_KEY in your .env file or pass it as env var.")
