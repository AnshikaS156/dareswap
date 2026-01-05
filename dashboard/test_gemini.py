from google import genai

client = genai.Client(api_key="YOUR_AI_STUDIO_API_KEY")

response = client.models.generate_content(
    model="gemini-1.5-pro",
    contents="Say hello in one sentence"
)

print(response.text)
