"""
ScholarshipGuide.pk — Daily AI Agent
Gemini API version (Free)
"""

import os
import json
import requests
from datetime import datetime

# ============================================
# CONFIG — GitHub Secrets mein yeh lagao
# ============================================
GEMINI_API_KEY   = os.environ.get("GEMINI_API_KEY")
AGENT_SECRET_KEY = os.environ.get("AGENT_SECRET_KEY")
WEBSITE_API_URL  = os.environ.get("WEBSITE_API_URL")

# ============================================
# STEP 1: Daily Topics List
# ============================================
def get_topic():
    topics = [
        "Rhodes Scholarship 2026 for Pakistani Students",
        "Erasmus Mundus Scholarship 2026 Complete Guide",
        "Korean Government Scholarship 2026 Pakistan",
        "How to get scholarship with low CGPA Pakistan",
        "IELTS preparation tips for scholarship applications",
        "How to write motivation letter for scholarship",
        "Japan MEXT Scholarship 2026 for Pakistani Students",
        "Sweden Scholarship 2026 for Pakistani Students",
        "How to get admission in German universities free",
        "Top 5 Easy Scholarships for Pakistani Students 2026",
        "Netherlands Orange Tulip Scholarship 2026",
        "How to apply for Chevening Scholarship step by step",
        "Fulbright Scholarship interview preparation tips",
        "Australian Awards Scholarship 2026 Pakistan guide",
        "How to write SOP for MS application Pakistan",
    ]
    # Har roz alag topic — din ke hisaab se
    day = datetime.now().day
    return topics[day % len(topics)]


# ============================================
# STEP 2: Gemini AI se Content Generate
# ============================================
def generate_content(topic):
    prompt = f"""You are a scholarship expert writing for Pakistani students.

Write a detailed blog post about: "{topic}"

Rules:
- Write in English
- Target audience: Pakistani students  
- Length: 600-800 words
- Use proper HTML tags: <h2>, <h3>, <p>, <ul>, <li>
- Include Pakistan-specific tips
- End with encouragement to apply

Return ONLY a JSON object, no extra text, no markdown:
{{
  "type": "post",
  "title": "...",
  "content": "...full HTML content...",
  "excerpt": "...2 line summary max 200 chars...",
  "category": "Guidance",
  "meta_title": "...max 60 chars...",
  "meta_description": "...max 150 chars...",
  "meta_keywords": "keyword1, keyword2, keyword3"
}}"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7}
    }

    response = requests.post(url, json=body)

    if response.status_code != 200:
        print(f"Gemini error: {response.text}")
        return None

    text = response.json()["candidates"][0]["content"]["parts"][0]["text"]

    # Clean JSON
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
        return None


# ============================================
# STEP 3: Website pe Upload
# ============================================
def upload_to_website(data):
    headers = {
        "Content-Type": "application/json",
        "X-Agent-Key": AGENT_SECRET_KEY
    }

    response = requests.post(WEBSITE_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print(f"Post uploaded: {result.get('slug')}")
            return True
        else:
            print(f"Upload failed: {result.get('error')}")
    else:
        print(f"HTTP Error: {response.status_code} — {response.text}")

    return False


# ============================================
# MAIN
# ============================================
def main():
    print(f"Agent start: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    topic = get_topic()
    print(f"Topic: {topic}")

    print("Generating content...")
    content = generate_content(topic)

    if not content:
        print("Content generation failed")
        return

    print(f"Title: {content.get('title')}")

    print("Uploading to website...")
    upload_to_website(content)

    print("Agent complete!")


if __name__ == "__main__":
    main()
