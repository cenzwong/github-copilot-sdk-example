from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="mock-key-not-validated-by-proxy"
)

completion = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[{"role": "user", "content": "Hi"}]
)
print(completion.choices[0].message.content)