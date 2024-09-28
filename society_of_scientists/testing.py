curl -X POST "https://api.ai21.com/v1/chat/completions" \
     -H "Authorization: Bearer 5AweiGc6E9UDXMCwtYDVhS5y6LarJoLl" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "jamba-1.5-large",
           "messages": [{"role": "user", "content": "Tell me about the first emperor of Rome"}],
           "max_tokens": 256,
           "temperature": 0.7
         }'
