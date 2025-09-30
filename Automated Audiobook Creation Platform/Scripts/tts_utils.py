import hashlib
import requests
from config import OPENAI_API_KEY, OPENAI_MODEL, CACHE_DIR

OPENAI_TTS_ENDPOINT = "https://api.openai.com/v1/audio/speech"

def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def synthesize_chunk_tts(text, out_path, voice=None, timeout=120):
    """
    Call OpenAI TTS and write binary audio to out_path.
    Uses /v1/audio/speech endpoint.
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "input": text
    }
    if voice:
        payload["voice"] = voice

    with requests.post(OPENAI_TTS_ENDPOINT, headers=headers, json=payload, stream=True, timeout=timeout) as r:
        if r.status_code != 200:
            raise RuntimeError(f"TTS failed: {r.status_code} - {r.text}")
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return out_path
