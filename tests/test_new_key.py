"""Test the new API key with available Jamba models."""
from ai21 import AI21Client
from ai21.models.chat import UserMessage
import requests
import json

new_key = "9f7fbfd0-52aa-460a-9cdb-66b39947a6b3"

print("=" * 60)
print("Testing New API Key")
print("=" * 60)

# Test 1: Check if key can list models
print("\n1. Testing models endpoint...")
try:
    response = requests.get(
        "https://api.ai21.com/studio/v1/models",
        headers={"Authorization": f"Bearer {new_key}"},
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   [OK] Key works! Found {len(data.get('data', []))} models")
        for model in data.get('data', []):
            print(f"      - {model['id']}: {model['name']}")
    else:
        print(f"   [FAIL] Error: {response.text[:100]}")
except Exception as e:
    print(f"   [FAIL] Error: {e}")

# Test 2: Try each available model
print("\n2. Testing available models...")
models_to_test = [
    "jamba-large-1.7-2025-07",
    "jamba-mini-2-2026-01",
    "jamba-mini-1.7-2025-07",
]

client = AI21Client(api_key=new_key)
working_models = []

for model in models_to_test:
    try:
        print(f"\n   Testing: {model}...", end=" ")
        messages = [UserMessage(content="Say 'API key works' if you can read this.")]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=50
        )
        
        if response and response.choices:
            content = response.choices[0].message.content
            print(f"[OK] Works!")
            print(f"      Response: {content[:80]}...")
            working_models.append(model)
        else:
            print("[FAIL] No response")
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg:
            print("[403] Access denied")
        elif "404" in error_msg:
            print("[404] Model not found")
        else:
            print(f"[ERROR] {error_msg[:50]}")

# Summary
print("\n" + "=" * 60)
print("Summary")
print("=" * 60)
if working_models:
    print(f"\n[OK] Working Models ({len(working_models)}):")
    for model in working_models:
        print(f"   - {model}")
    print(f"\n✅ This key works! You can use: {working_models[0]}")
else:
    print("\n[FAIL] No working models found")
    print("The key may not have access to Jamba models")
