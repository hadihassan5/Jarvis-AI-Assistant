from openai import OpenAI

client = OpenAI(
    api_key="API KEY"   
)

completions = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "You are a virtual assistant Jarvis."},
        {"role": "user", "content": "Write a one-sentence bedtime story about a unicorn."}
    ]
)

print(completions.choices[0].message.content)
