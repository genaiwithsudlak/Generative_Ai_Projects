
# AI-Powered Document/Book Intelligence System (2025)

Project scaffold extracted from a single-file Streamlit app. The codebase is modularized into multiple scripts so it's easy to maintain, test and publish to GitHub without looking like a single-line generated file.

## Features
- One-time QA + Summarizer (no persistent storage)
- Recommender (calls out to an LLM API like Mistral — API key required)
- Domain-specific Fine-tuning (placeholder)
- Persistent Knowledge Assistant (RAG) using Chroma / FAISS

## Quickstart (development)
1. Copy `.env.example` to `.env` and fill keys (MISTRAL_API_KEY etc).
2. Create a Python venv: `python -m venv .venv && source .venv/bin/activate`
3. Install requirements: `pip install -r requirements.txt`
4. Run: `streamlit run app/streamlit_app.py`

## Project structure
- `app/` - main Streamlit application and entrypoint
- `app/modules/` - modular components: loaders, embeddings, qa, rag, recommender, finetune
- `requirements.txt` - Python dependencies
- `.env.example` - example environment variables
- `.gitignore` - sensible ignores

## Notes
- This scaffold keeps the same logical flow as your original app but splits responsibilities.
- Fine-tuning and heavy model calls are left as placeholders or example functions to avoid accidental long-running operations.
