import os
import requests
import json
from openai import OpenAI

# Retrieve the API token from environment variables
token = os.environ["GITHUB_TOKEN"]
news_key = os.environ["NEWS_KEY"]

# Define the endpoint and model name
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

def search_news(query, api_key):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('articles', [])
    else:
        return None

# Initialization
client = OpenAI(
    base_url=endpoint,
    api_key=token,
)
userQ = input("Enter your question: ")

context = json.dumps(search_news(userQ, news_key)[:3]) # Get the first 3 news articles
# Query the API
response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant. You must only answer questions about the news, using this content as context: " + context,
        },
        {
            "role": "user",
            "content": userQ,
        }
    ],
    model=model_name,
)
print(response.choices[0].message.content)