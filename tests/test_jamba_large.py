"""Test jamba-large model name with the new key."""
from ai21 import AI21Client
from ai21.models.chat import UserMessage

new_key = "9f7fbfd0-52aa-460a-9cdb-66b39947a6b3"

print("=" * 60)
print("Testing 'jamba-large' Model")
print("=" * 60)

try:
    client = AI21Client(api_key=new_key)
    
    print("\nTesting model: jamba-large")
    print("API Key:", new_key[:20] + "...")
    
    messages = [UserMessage(content="Say 'API key works' if you can read this.")]
    response = client.chat.completions.create(
        model="jamba-large",
        messages=messages,
        max_tokens=50,
        temperature=0.7
    )
    
    if response and response.choices:
        content = response.choices[0].message.content
        print(f"\n[OK] SUCCESS! Model 'jamba-large' works!")
        print(f"\nResponse: {content}")
        print(f"\n✅ You can use 'jamba-large' as the model name!")
    else:
        print("\n[FAIL] No response received")
        
except Exception as e:
    error_msg = str(e)
    print(f"\n[ERROR] {error_msg}")
    
    if "403" in error_msg:
        print("\n[403] Access denied - Account may not have access to this model")
    elif "404" in error_msg:
        print("\n[404] Model not found - 'jamba-large' may not be the correct name")
    else:
        print(f"\nFull error details above")
