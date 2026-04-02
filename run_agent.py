import os, json, requests
from datetime import datetime

API_KEY = os.environ.get("GEMINI_API_KEY")
SECRET  = os.environ.get("AGENT_SECRET_KEY")
API_URL = os.environ.get("WEBSITE_API_URL")

topics = ["Rhodes Scholarship 2026 Pakistan","Erasmus Mundus 2026 Guide","Korean Government Scholarship 2026","Low CGPA scholarship tips Pakistan","IELTS tips for scholarships","Motivation letter writing guide","Japan MEXT Scholarship 2026","Sweden Scholarship 2026 Pakistan","Free education Germany Pakistan","Easy scholarships 2026 Pakistan","Netherlands Scholarship 2026","Chevening apply step by step","Fulbright interview tips","Australia Awards 2026 Pakistan","SOP writing guide Pakistan"]
topic = topics[datetime.now().day % len(topics)]
print(f"Topic: {topic}")

prompt = f"""Write a blog post for Pakistani students about: {topic}
Return ONLY JSON:
{{"type":"post","title":"...","content":"...HTML...","excerpt":"...","category":"Guidance","meta_title":"...","meta_description":"...","meta_keywords":"..."}}"""

r = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://scholarshipsguide.xyz"
    },
    json={"model":"mistralai/mistral-7b-instruct:free","messages":[{"role":"user","content":prompt}]}
)

print(f"Status: {r.status_code}")
if r.status_code != 200:
    print(r.text)
    exit()

text = r.json()["choices"][0]["message"]["content"]
text = text.replace("```json","").replace("```","").strip()

try:
    data = json.loads(text)
    print(f"Title: {data.get('title')}")
    res = requests.post(API_URL, headers={"Content-Type":"application/json","X-Agent-Key":SECRET}, json=data)
    print(res.json())
except Exception as e:
    print(f"Error: {e}")
    print(f"Raw: {text[:200]}")
