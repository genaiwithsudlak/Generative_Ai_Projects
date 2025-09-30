# backend/app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from services.genai import generate_resume_and_cover
from services.jd_fetcher import fetch_jd_from_linkedin
from ..config import settings

app = FastAPI(title="AI Job Application MVP")

class GenerateRequest(BaseModel):
    user_profile: Dict[str, Any]
    jd_text: Optional[str] = None
    job_url: Optional[str] = None
    use_linkedin_credentials: Optional[bool] = False

@app.post("/v1/generate")
def generate(req: GenerateRequest):
    jd_text = req.jd_text
    if req.job_url and not jd_text:
        # If user wants us to fetch, require credentials in settings or raise error
        if settings.LINKEDIN_EMAIL and settings.LINKEDIN_PASSWORD:
            jd_text = fetch_jd_from_linkedin(req.job_url, settings.LINKEDIN_EMAIL, settings.LINKEDIN_PASSWORD)
        else:
            raise HTTPException(status_code=400, detail="No JD text provided and no LinkedIn credentials configured. Paste jd_text or set LINKEDIN_EMAIL/PASSWORD in .env for local use.")
    if not jd_text:
        raise HTTPException(status_code=400, detail="Provide jd_text or job_url (with local credentials configured).")

    result = generate_resume_and_cover(user_profile=req.user_profile, jd_text=jd_text)
    # At this point you can call a formatter to create DOCX/PDF; MVP returns JSON
    return {"status":"ok", "result": result}
