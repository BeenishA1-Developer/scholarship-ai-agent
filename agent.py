"""
ScholarshipGuide.pk — Daily AI Agent
Har roz:
1. Trending scholarship keywords search karta hai
2. Claude AI se content likhwata hai
3. Website pe post upload karta hai
"""

import os
import json
import requests
from datetime import datetime

# ============================================
# CONFIG — GitHub Secrets mein yeh lagao
# ============================================
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
AGENT_SECRET_KEY  = os.environ.get("AGENT_SECRET_KEY")   # same as PHP file mein
WEBSITE_API_URL   = os.environ.get("WEBSITE_API_URL")    # https://scholarshipsguide.xyz/api/agent_post.php
SERPAPI_KEY       = os.environ.get("SERPAPI_KEY")        # Free at serpapi.com

# ============================================
# STEP 1: Trending Keywords Search
# ============================================
def get_trending_keywords():
    """Google pe scholarship keywords search karo"""
    
    queries = [
        "fully funded scholarships 2026 for Pakistani students",
        "new scholarships open 2026 Pakistan",
        "scholarship deadlines 2026 Pakistan apply"
    ]
    
    results = []
    
    if not SERPAPI_KEY:
        # SerpAPI nahi hai toh default topics use karo
        print("SerpAPI key nahi hai — default topics use kar raha hun")
        return [
            "Rhodes Scholarship 2026",
            "Erasmus Mundus Scholarship 2026",
            "Korean Government Scholarship 2026",
            "Australia Awards Scholarship 2026 Pakistan",
            "How to get scholarship with low CGPA Pakistan"
        ]
    
    for query in queries[:1]:  # 1 query enough hai free plan pe
        try:
            response = requests.get("https://serpapi.com/search", params={
                "q": query,
                "api_key": SERPAPI_KEY,
                "num": 5
            })
            data = response.json()
            for result in data.get("organic_results", []):
                results.append(result.get("title", ""))
        except Exception as e:
            print(f"Search error: {e}")
    
    return results if results else ["Top Scholarships for Pakistani Students 2026"]


# ============================================
# STEP 2: Claude AI se Content Generate
# ============================================
def generate_content_with_claude(topic, content_type="post"):
    """Claude API se content likhwao"""
    
    today = datetime.now().strftime("%B %Y")
    
    if content_type == "post":
        prompt = f"""
You are a scholarship expert writing for Pakistani students.

Write a detailed blog post about: "{topic}"

Rules:
- Write in English
- Target audience: Pakistani students
- Length: 600-800 words
- Use proper HTML tags: <h2>, <h3>, <p>, <ul>, <li>
- Mention Pakistan-specific tips where relevant
- End with a call to action to check scholarshipsguide.xyz

Return ONLY a JSON object (no extra text):
{{
  "type": "post",
  "title": "...",
  "content": "...full HTML content...",
  "excerpt": "...2 line summary...",
  "category": "Guidance",
  "meta_title": "...",
  "meta_description": "...150 chars...",
  "meta_keywords": "keyword1, keyword2, keyword3"
}}
"""
    else:
        prompt = f"""
You are a scholarship expert for Pakistani students.

Research and write about this scholarship: "{topic}"

Return ONLY a JSON object (no extra text):
{{
  "type": "scholarship",
  "title": "Scholarship Name 2026 - Country Fully Funded",
  "country": "...",
  "level": "MS" or "BS, MS, PhD",
  "funding_type": "Fully Funded",
  "host_university": "...",
  "deadline": "2026-XX-XX",
  "amount": "Full Tuition + stipend details",
  "benefits": "benefit1\\nbenefit2\\nbenefit3",
  "eligibility": "requirement1\\nrequirement2",
  "how_to_apply": "step1\\nstep2\\nstep3",
  "official_link": "https://...",
  "category_id": 1,
  "meta_title": "...",
  "meta_description": "...150 chars...",
  "meta_keywords": "keyword1, keyword2"
}}
"""

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    body = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=body
    )
    
    if response.status_code != 200:
        print(f"Claude API error: {response.text}")
        return None
    
    text = response.json()["content"][0]["text"]
    
    # JSON parse karo
    try:
        # Code block hata do agar ho
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Response was: {text[:200]}")
        return None


# ============================================
# STEP 3: Website pe Post Upload
# ============================================
def upload_to_website(data):
    """API call karo aur post upload karo"""
    
    headers = {
        "Content-Type": "application/json",
        "X-Agent-Key": AGENT_SECRET_KEY
    }
    
    response = requests.post(
        WEBSITE_API_URL,
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success"):
            print(f"✅ Post uploaded: {result.get('slug')}")
            return True
        else:
            print(f"❌ Upload failed: {result.get('error')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
    
    return False


# ============================================
# MAIN — Daily Run
# ============================================
def main():
    print(f"🤖 Agent start: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Step 1: Keywords lo
    print("🔍 Keywords search kar raha hun...")
    topics = get_trending_keywords()
    print(f"   Topics mila: {len(topics)}")
    
    # Step 2: Ek blog post banao
    topic = topics[0] if topics else "Study Abroad Guide for Pakistani Students 2026"
    print(f"✍️  Post likh raha hun: {topic}")
    
    content = generate_content_with_claude(topic, content_type="post")
    
    if not content:
        print("❌ Content generate nahi hua")
        return
    
    print(f"   Title: {content.get('title', 'N/A')}")
    
    # Step 3: Upload karo
    print("📤 Website pe upload kar raha hun...")
    upload_to_website(content)
    
    print("✅ Agent complete!")


if __name__ == "__main__":
    main()
