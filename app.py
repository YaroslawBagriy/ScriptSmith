import openai
import os
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

# Create OpenAI client
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']  
)

# Create a call using the completions API
completion = client.chat.completions.create(
  model="gpt-4.1",
  messages=[
    {"role": "user", "content": "What are the benefits of using serverless architecture?"} # User message
  ]
)

print(completion.model_dump_json(indent=2))

print(completion.choices[0].message.content)

# Add a system message with tone control (Prompt engineering)
completion = client.chat.completions.create(
  model="gpt-4.1",
  messages=[
    {"role": "system", "content": "You are a Cloud Architect familiar with AWS. You specialize in accurate and concise answers."}, # System message
    {"role": "user", "content": "What are the benefits of using serverless architecture?"} # User message
  ]
)

print(completion.choices[0].message.content)

completion = client.chat.completions.create(
  model="gpt-4.1",
  temperature=0.7, #between 0 and 1; closer to 1 more creative and random
  max_tokens=100, #number of output tokens
  messages=[
    {"role": "system", "content": "You are a Cloud Architect familiar with AWS. You specialize in accurate and concise answers."}, # System message
    {"role": "user", "content": "What are the benefits of using serverless architecture?"} # User message
  ]
) 

print(completion.choices[0].message.content)