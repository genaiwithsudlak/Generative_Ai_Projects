# backend/app/services/jd_fetcher.py
from bs4 import BeautifulSoup
import logging
from typing import Optional
from ..config import settings

# Playwright import
from playwright.sync_api import sync_playwright

def fetch_jd_from_linkedin(job_url: str, email: Optional[str]=None, password: Optional[str]=None) -> str:
    """
    Best-effort: logs into LinkedIn (if creds provided) and returns the visible job description text.
    WARNING: Use locally and with your consent. Don't store credentials in code.
    """
    if email is None or password is None:
        raise ValueError("LinkedIn credentials required for remote scraping. Prefer to paste jd_text instead.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.linkedin.com/login", wait_until="networkidle")
        # Fill in login form — selectors may change
        page.fill('input[name="session_key"]', email)
        page.fill('input[name="session_password"]', password)
        page.click('button[type="submit"]')
        page.wait_for_load_state("networkidle")
        page.goto(job_url, wait_until="networkidle")

        # Try common selectors for LinkedIn job descriptions
        try:
            # LinkedIn frequently wraps JD in a div with role="main" or specific data-test attributes
            content = ""
            # attempt multiple selectors
            selectors = [
                'div[data-job-id]', # not guaranteed
                'div[class*="description"]',
                'div.jobs-description__container',
                'div[role="main"]'
            ]
            for sel in selectors:
                elems = page.query_selector_all(sel)
                if elems:
                    for e in elems:
                        txt = e.inner_text().strip()
                        if txt and len(txt) > len(content):
                            content = txt
            if not content:
                # fallback: grab body text
                content = page.content()
                soup = BeautifulSoup(content, "html.parser")
                content = soup.get_text(separator="\n")
        finally:
            browser.close()
    return content
