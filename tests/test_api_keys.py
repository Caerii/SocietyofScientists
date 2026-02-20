"""Test script to verify API keys are working."""
import sys
import os

# Add society_of_scientists to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'society_of_scientists'))

def test_ai21_key():
    """Test AI21 Jamba API key."""
    print("Testing AI21 API key...")
    try:
        from ai21 import AI21Client
        from ai21.models.chat import UserMessage
        
        # Test key from jamba_working.py
        api_key = "5AweiGc6E9UDXMCwtYDVhS5y6LarJoLl"
        client = AI21Client(api_key=api_key)
        
        # Simple test call using the correct format
        messages = [UserMessage(content="Say 'API key works' if you can read this.")]
        response = client.chat.completions.create(
            model="jamba-1.5-large",
            messages=messages,
            max_tokens=50
        )
        
        if response and response.choices:
            content = response.choices[0].message.content
            print(f"[OK] AI21 API key works! Response: {content[:100]}")
            return True
        else:
            print("[FAIL] AI21 API key test failed - no response")
            return False
    except Exception as e:
        print(f"[FAIL] AI21 API key test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_exa_key():
    """Test Exa API key."""
    print("\nTesting Exa API key...")
    try:
        from exa_py import Exa
        
        # Test key from exa_files.py
        api_key = "03af6e3c-7b7f-4d46-b541-6771b8a240e0"
        exa = Exa(api_key=api_key)
        
        # Simple test search
        result = exa.search(
            query="test",
            num_results=1,
            type="neural"
        )
        
        if result and hasattr(result, 'results'):
            print(f"[OK] Exa API key works! Found {len(result.results)} results")
            return True
        else:
            print("[FAIL] Exa API key test failed - no results")
            return False
    except Exception as e:
        print(f"[FAIL] Exa API key test failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("API Key Verification Test")
    print("=" * 50)
    
    ai21_works = test_ai21_key()
    exa_works = test_exa_key()
    
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  AI21 Key: {'[OK] Working' if ai21_works else '[FAIL] Failed'}")
    print(f"  Exa Key:  {'[OK] Working' if exa_works else '[FAIL] Failed'}")
    print("=" * 50)
