import os
"""Try to get available models from AI21 API directly."""
import requests
import json

api_key = os.getenv("AI21_API_KEY", "")

print("=" * 60)
print("Checking AI21 API for Available Models")
print("=" * 60)

# Try different endpoints
endpoints = [
    "https://api.ai21.com/studio/v1/models",
    "https://api.ai21.com/v1/models",
    "https://api.ai21.com/models",
    "https://studio.ai21.com/api/v1/models",
]

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

for endpoint in endpoints:
    print(f"\nTrying: {endpoint}")
    try:
        response = requests.get(endpoint, headers=headers, timeout=5)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  [OK] Success! Response:")
                print(json.dumps(data, indent=2))
                break
            except:
                print(f"  Response text: {response.text[:200]}")
        elif response.status_code == 401:
            print("  [401] Unauthorized - Key might be invalid")
        elif response.status_code == 403:
            print("  [403] Forbidden - Key doesn't have access")
        else:
            print(f"  Response: {response.text[:200]}")
    except Exception as e:
        print(f"  Error: {e}")

# Also try the completion endpoint to see what models it accepts
print("\n" + "=" * 60)
print("Checking what models work via completion endpoint")
print("=" * 60)

# Based on AI21 docs, common model names
common_models = [
    "jamba-1.5-large",
    "jamba-1.5-mini", 
    "j2-ultra",
    "j2-mid",
    "j2-light",
    "jamba-instruct",
]

for model in common_models:
    try:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 1
        }
        response = requests.post(
            "https://api.ai21.com/studio/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"[OK] {model} - Works!")
        elif response.status_code == 404:
            print(f"[404] {model} - Not found")
        elif response.status_code == 403:
            print(f"[403] {model} - Access denied")
        else:
            print(f"[{response.status_code}] {model} - {response.text[:50]}")
    except Exception as e:
        print(f"[ERROR] {model} - {e}")
