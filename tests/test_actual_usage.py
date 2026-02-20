"""Test actual usage patterns from the codebase."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'society_of_scientists'))

print("=" * 60)
print("Testing Actual Code Usage Patterns")
print("=" * 60)

# Test 1: Exa search tool (from tools.py)
print("\n1. Testing Exa search tool (from tools.py)...")
try:
    from exa_py import Exa
    
    exa = Exa(api_key="03af6e3c-7b7f-4d46-b541-6771b8a240e0")
    result = exa.search_and_contents(
        "computational neuroscience",
        type="neural",
        num_results=2,
        summary={"query": "What does this paper cover?"},
        category="research paper",
        exclude_domains=["en.wikipedia.org"],
        start_published_date="2023-01-01",
        text={"include_html_tags": True},
        highlights=True
    )
    
    if result and hasattr(result, 'results') and len(result.results) > 0:
        print(f"   [OK] Exa search works! Found {len(result.results)} papers")
        print(f"   First paper: {result.results[0].title[:60]}...")
    else:
        print("   [FAIL] No results returned")
except Exception as e:
    print(f"   [FAIL] Error: {e}")

# Test 2: AI21 Jamba client (from jamba_working.py pattern)
print("\n2. Testing AI21 Jamba client (from jamba_working.py)...")
try:
    from ai21 import AI21Client
    from ai21.models.chat import UserMessage
    from types import SimpleNamespace
    
    api_key = "5AweiGc6E9UDXMCwtYDVhS5y6LarJoLl"
    client = AI21Client(api_key=api_key)
    
    # Try the exact pattern from jamba_working.py
    messages = [UserMessage(content="Hello, this is a test.")]
    response = client.chat.completions.create(
        model="jamba-1.5-large",
        messages=messages,
        temperature=0.7,
        top_p=1.0,
        max_tokens=50
    )
    
    if response and response.choices:
        content = response.choices[0].message.content
        print(f"   [OK] AI21 Jamba works! Response: {content[:60]}...")
    else:
        print("   [FAIL] No response")
except Exception as e:
    print(f"   [FAIL] Error: {e}")
    # Try alternative models
    print("   Trying alternative models...")
    for model in ["jamba-instruct", "jamba-1.5-mini", "j2-ultra"]:
        try:
            client = AI21Client(api_key=api_key)
            messages = [UserMessage(content="Test")]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=10
            )
            if response:
                print(f"   [OK] Model '{model}' works!")
                break
        except:
            pass

# Test 3: Test cached data loading
print("\n3. Testing cached data loading...")
try:
    from society_of_scientists.tools import load_research_summaries, get_summary_count
    
    counts = get_summary_count()
    total = sum(counts.values())
    print(f"   [OK] Cached data available: {total} summaries total")
    for topic, count in counts.items():
        print(f"      - {topic}: {count} summaries")
except Exception as e:
    print(f"   [FAIL] Error: {e}")

print("\n" + "=" * 60)
print("Summary: All key functionality tested")
print("=" * 60)
