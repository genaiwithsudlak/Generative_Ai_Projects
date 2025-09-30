# backend/app/services/genai.py
import json
from typing import Any, Dict
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

from ..config import settings

# Initialize LLM client
llm = ChatOpenAI(temperature=0.1, model=settings.LLM_MODEL, openai_api_key=settings.OPENAI_API_KEY)

resume_prompt = PromptTemplate(
    input_variables=["user_profile", "jd_text"],
    template="""
You are an expert resume writer and recruiter.

Input user_profile (JSON):
{user_profile}

Job description:
{jd_text}

Produce output in JSON with exactly two keys: "resume" and "cover_letter".
- "resume" should be a JSON object with keys: name, contact, summary (1-2 lines), work_experience (list of objects {role, company, start, end, bullets}), projects (list), skills (list).
- "cover_letter" should be a plain text 3-paragraph cover letter tailored to the JD.

Return valid JSON only (no explanation).
"""
)

chain = LLMChain(llm=llm, prompt=resume_prompt)

def generate_resume_and_cover(user_profile: Dict[str,Any], jd_text: str) -> Dict[str,Any]:
    # Convert user_profile to JSON string for prompt clarity
    user_profile_json = json.dumps(user_profile, indent=2)
    out_text = chain.run({"user_profile": user_profile_json, "jd_text": jd_text})

    # Try to parse JSON from model output safely
    try:
        parsed = json.loads(out_text)
    except Exception:
        # best-effort: try to extract JSON substring
        import re
        m = re.search(r"\{[\s\S]*\}\s*$", out_text)
        if m:
            try:
                parsed = json.loads(m.group(0))
            except Exception:
                parsed = {"raw": out_text}
        else:
            parsed = {"raw": out_text}
    return parsed
