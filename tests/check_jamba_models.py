"""Check available Jamba models from AI21 API."""
import sys
import os

try:
    from ai21 import AI21Client
    from ai21.models.chat import UserMessage
    
    api_key = os.getenv("AI21_API_KEY", "")
    client = AI21Client(api_key=api_key)
    
    print("=" * 60)
    print("Checking Available Jamba Models")
    print("=" * 60)
    
    # List of potential Jamba model names to test
    potential_models = [
        "jamba-1.5-large",
        "jamba-1.5-mini",
        "jamba-1.5-small",
        "jamba-1.5-medium",
        "jamba-1.5-instruct",
        "jamba-instruct",
        "jamba-large",
        "jamba-mini",
        "jamba-small",
        "jamba-medium",
        "jamba-1.5",
        "jamba",
    ]
    
    print("\nTesting potential model names...")
    working_models = []
    failed_models = []
    
    for model in potential_models:
        try:
            print(f"\nTesting: {model}...", end=" ")
            messages = [UserMessage(content="test")]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=10
            )
            if response and response.choices:
                print(f"[OK] Works!")
                working_models.append(model)
            else:
                print(f"[FAIL] No response")
                failed_models.append(model)
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg or "Access denied" in error_msg:
                print(f"[403] Access denied")
                failed_models.append((model, "403"))
            elif "404" in error_msg or "not found" in error_msg.lower():
                print(f"[404] Not found")
                failed_models.append((model, "404"))
            else:
                print(f"[ERROR] {error_msg[:50]}")
                failed_models.append((model, error_msg[:50]))
    
    print("\n" + "=" * 60)
    print("Results Summary")
    print("=" * 60)
    
    if working_models:
        print(f"\n[OK] Working Models ({len(working_models)}):")
        for model in working_models:
            print(f"   - {model}")
    else:
        print("\n[FAIL] No working models found")
    
    print(f"\n[FAIL] Failed/Not Available ({len(failed_models)}):")
    for item in failed_models:
        if isinstance(item, tuple):
            model, reason = item
            print(f"   - {model}: {reason}")
        else:
            print(f"   - {item}")
    
    # Try to get model list from API if available
    print("\n" + "=" * 60)
    print("Attempting to list models from API...")
    print("=" * 60)
    try:
        # Some APIs have a models endpoint
        import requests
        response = requests.get(
            "https://api.ai21.com/studio/v1/models",
            headers={"Authorization": f"Bearer {api_key}"}
        )
        if response.status_code == 200:
            models_data = response.json()
            print("Available models from API:")
            print(models_data)
        else:
            print(f"Could not fetch models list: {response.status_code}")
    except Exception as e:
        print(f"Could not fetch models list: {e}")
    
except ImportError:
    print("ai21 package not installed. Install with: uv pip install ai21")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
