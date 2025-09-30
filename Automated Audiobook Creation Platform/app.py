import time
import streamlit as st
from Scripts.config import CACHE_DIR, OUT_DIR, DEFAULT_VOICE, CHUNK_MAX_CHARS, CHUNK_OVERLAP
from Scripts.pdf_utils import extract_text_from_pdf_bytes
from Scripts.chunk_utils import simple_chunker
from Scripts.tts_utils import sha256_text, synthesize_chunk_tts
from Scripts.audio_utils import combine_mp3_files

st.set_page_config(page_title="Automated Audiobook Creator", layout="wide")
st.title("Automated Audiobook Creation Platform — Modular Demo")

with st.sidebar:
    st.header("Settings")
    max_chars = st.number_input("Chunk max characters", min_value=1000, max_value=10000, value=CHUNK_MAX_CHARS, step=500)
    overlap = st.number_input("Chunk overlap (chars)", min_value=0, max_value=1000, value=CHUNK_OVERLAP, step=50)
    voice = st.text_input("Voice (optional)", value=DEFAULT_VOICE)
    preview_pages = st.slider("Preview pages (demo only)", min_value=1, max_value=20, value=3)
    generate_full = st.checkbox("Generate full audiobook (costly)", value=False)

uploaded_file = st.file_uploader("Upload PDF book", type=["pdf"])

if uploaded_file:
    bytes_data = uploaded_file.read()
    with st.spinner("Extracting text..."):
        text, total_pages = extract_text_from_pdf_bytes(bytes_data)
    st.success(f"Extracted text from {total_pages} pages.")

    if not generate_full:
        st.info(f"Preview mode: Synthesizing first {preview_pages} pages.")
        pages = text.split("\n\n")
        target_text = "\n\n".join(pages[:preview_pages])
    else:
        target_text = text

    if st.button("Create Audiobook"):
        chunks = simple_chunker(target_text, max_chars=max_chars, overlap=overlap)
        st.write(f"Split into {len(chunks)} chunks.")

        mp3_chunk_paths = []
        progress = st.progress(0)

        for i, chunk in enumerate(chunks, start=1):
            chunk_hash = sha256_text(chunk)
            cached_file = CACHE_DIR / f"{chunk_hash}.mp3"
            if cached_file.exists():
                mp3_chunk_paths.append(str(cached_file))
            else:
                try:
                    synthesize_chunk_tts(chunk, str(cached_file), voice=voice)
                    mp3_chunk_paths.append(str(cached_file))
                except Exception as e:
                    st.error(f"Error in chunk {i}: {e}")
                    break

            progress.progress(int(i / len(chunks) * 100))
            time.sleep(0.1)

        if mp3_chunk_paths:
            out_filename = f"{uploaded_file.name.rsplit('.',1)[0]}_audiobook.mp3"
            out_path = OUT_DIR / out_filename
            combine_mp3_files(mp3_chunk_paths, str(out_path))
            st.success("Audiobook created!")
            audio_bytes = out_path.read_bytes()
            st.audio(audio_bytes)
            st.download_button("Download Audiobook", audio_bytes, file_name=out_filename, mime="audio/mpeg")
