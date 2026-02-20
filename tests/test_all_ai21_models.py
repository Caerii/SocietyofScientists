"""Test all possible AI21 models with the new key."""
from ai21 import AI21Client
from ai21.models.chat import UserMessage

new_key = "9f7fbfd0-52aa-460a-9cdb-66b39947a6b3"
client = AI21Client(api_key=new_key)

print("=" * 60)
print("Testing All AI21 Models")
print("=" * 60)

# All known AI21 models
all_models = [
    # Jamba models
    "jamba-large-1.7-2025-07",
    "jamba-mini-2-2026-01",
    "jamba-mini-1.7-2025-07",
    "jamba-1.5-large",
    "jamba-1.5-mini",
    "jamba-instruct",
    
    # J2 models (older AI21 models)
    "j2-ultra",
    "j2-mid",
    "j2-light",
    "j2-ultra-v1",
    "j2-mid-v1",
    "j2-light-v1",
    
    # Other possible names
    "jamba",
    "jamba-large",
    "jamba-mini",
]

working_models = []
failed_models = []

for model in all_models:
    try:
        print(f"\nTesting: {model:30}...", end=" ")
        messages = [UserMessage(content="test")]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=10
        )
        
        if response and response.choices:
            content = response.choices[0].message.content
            print(f"[OK] Works!")
            working_models.append(model)
        else:
            print("[FAIL] No response")
            failed_models.append((model, "no response"))
    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg:
            print("[403] Access denied")
            failed_models.append((model, "403"))
        elif "404" in error_msg or "not found" in error_msg.lower():
            print("[404] Not found")
            failed_models.append((model, "404"))
        else:
            print(f"[ERROR] {error_msg[:40]}")
            failed_models.append((model, error_msg[:40]))

print("\n" + "=" * 60)
print("Results")
print("=" * 60)

if working_models:
    print(f"\n[OK] Working Models ({len(working_models)}):")
    for model in working_models:
        print(f"   ✅ {model}")
    print(f"\n🎉 SUCCESS! Use this model: {working_models[0]}")
else:
    print("\n[FAIL] No working models found")
    print("\nThe key can query the API but doesn't have access to use any models.")
    print("This suggests:")
    print("  - Account needs model access enabled")
    print("  - Billing/payment setup required")
    print("  - Account may be in trial/limited mode")

print(f"\nTotal tested: {len(all_models)}")
print(f"Working: {len(working_models)}")
print(f"Failed: {len(failed_models)}")
