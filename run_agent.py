import os, json, requests
from datetime import datetime

# GitHub Secret GEMINI_API_KEY = (Your OpenRouter Key sk-or-v1-...)
OPENROUTER_API_KEY = os.environ.get("GEMINI_API_KEY")
SECRET  = os.environ.get("AGENT_SECRET_KEY")
API_URL = os.environ.get("WEBSITE_API_URL")

topics = ["Rhodes Scholarship 2026 Pakistan","Erasmus Mundus 2026 Guide","Korean Government Scholarship 2026","Low CGPA scholarship tips Pakistan","IELTS tips for scholarships","Motivation letter writing guide","Japan MEXT Scholarship 2026","Sweden Scholarship 2026 Pakistan","Free education Germany Pakistan","Easy scholarships 2026 Pakistan","Netherlands Scholarship 2026","Chevening apply step by step","Fulbright interview tips","Australia Awards 2026 Pakistan","SOP writing guide Pakistan"]

def main():
    if not OPENROUTER_API_KEY:
        print("[Error] GEMINI_API_KEY secret is not set.")
        return

    topic = topics[datetime.now().day % len(topics)]
    print(f"[*] Topic: {topic}")

    prompt = f"""Write a blog post for Pakistani students exploring: {topic}
Return exactly ONE valid JSON object and NOTHING else. No markdown formatting.
{{
  "type":"post",
  "title":"...",
  "content":"...HTML formatted text...",
  "excerpt":"...",
  "category":"Guidance",
  "meta_title":"...",
  "meta_description":"...",
  "meta_keywords":"..."
}}"""

    print("[*] Requesting OpenRouter API...")
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://scholarshipsguide.xyz"
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=120
        )
    except Exception as e:
        print(f"[Error] OpenRouter connection failed: {e}")
        return

    print(f"[*] OpenRouter Status: {r.status_code}")
    if r.status_code != 200:
        print(f"[Error] OpenRouter Response: {r.text}")
        return

    text = r.json()["choices"][0]["message"]["content"]
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(text)
        print(f"[*] Generated Title: {data.get('title')}")
    except json.JSONDecodeError:
        print("[Error] Invalid JSON from OpenRouter:")
        print(text[:200])
        return

    print(f"[*] Sending post to your website ({API_URL})...")
    try:
        res = requests.post(API_URL, headers={"Content-Type":"application/json","X-Agent-Key":SECRET}, json=data)
        res_text = res.text
        
        print(f"[*] Website Status: {res.status_code}")
        try:
            print(f"[*] Website Response: {res.json()}")
        except:
            print(f"[*] Website Raw Response: {res_text}")
            
        # VERY IMPORTANT CHECK
        if "googleapis.com" in res_text or "Gemini" in res_text:
            print("\n" + "="*50)
            print("🚨 IMPORTANT ALERT FOR BEENISH:")
            print("The 'Gemini error: API key not valid - googleapis.com' is NOT coming from this Python script!")
            print("It is coming from your WEBSITE'S PHP FILE ('agent_post.php')!")
            print("Your Python script successfully used OpenRouter and sent the data to the website.")
            print("But your website tried to connect to Google/Gemini (maybe for an image or tags) and failed.")
            print("Please check your WooCommerce/WordPress or 'agent_post.php' code on your server.")
            print("="*50 + "\n")
            
    except Exception as e:
        print(f"[Error] Failed to connect to website API: {e}")

if __name__ == "__main__":
    main()
