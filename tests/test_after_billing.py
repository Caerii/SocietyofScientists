import os

"""Test both API keys after billing connection."""
from ai21 import AI21Client
from ai21.models.chat import UserMessage

keys_to_test = [
    ("Original Key", os.getenv("AI21_API_KEY", "")),
    ("New Key", os.getenv("AI21_NEW_API_KEY", "")),
]

models_to_test = [
    "jamba-large",
    "jamba-large-1.7-2025-07",
    "jamba-mini-2-2026-01",
    "jamba-mini-1.7-2025-07",
]

print("=" * 70)
print("Testing API Keys After Billing Connection")
print("=" * 70)

working_combinations = []

for key_name, api_key in keys_to_test:
    print(f"\n{'=' * 70}")
    print(f"Testing: {key_name}")
    print(f"{'=' * 70}")

    client = AI21Client(api_key=api_key)

    for model in models_to_test:
        try:
            print(f"\n  Testing {model:30}...", end=" ")
            messages = [
                UserMessage(content="Say 'API key works' if you can read this.")
            ]
            response = client.chat.completions.create(
                model=model, messages=messages, max_tokens=50, temperature=0.7
            )

            if response and response.choices:
                content = response.choices[0].message.content
                print(f"[OK] WORKS!")
                print(f"      Response: {content[:80]}...")
                working_combinations.append((key_name, model, content))
            else:
                print("[FAIL] No response")
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg:
                print("[403] Still access denied")
            elif "404" in error_msg:
                print("[404] Model not found")
            else:
                print(f"[ERROR] {error_msg[:40]}")

print("\n" + "=" * 70)
print("FINAL RESULTS")
print("=" * 70)

if working_combinations:
    print(f"\n[SUCCESS] Found {len(working_combinations)} working combination(s):\n")
    for key_name, model, response in working_combinations:
        print(f"  ✅ {key_name}")
        print(f"     Model: {model}")
        print(f"     Response preview: {response[:60]}...")
        print()

    # Recommend the first working one
    best_key, best_model, _ = working_combinations[0]
    print(f"\n🎉 RECOMMENDATION:")
    print(f"   Use Key: {best_key}")
    print(f"   Use Model: {best_model}")
    print(f"\n   Update jamba_working.py:")
    print(f"   - Line 22: Change model to '{best_model}'")
    print(f"   - Keep API key as is")
else:
    print("\n[FAIL] No working combinations found")
    print("\nEven after billing connection, models still return 403.")
    print("This might mean:")
    print("  - Billing needs time to propagate")
    print("  - Account needs explicit model access enabled")
    print("  - May need to wait a few minutes for activation")
