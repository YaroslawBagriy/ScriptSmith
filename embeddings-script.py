# Capture relationships between concepts
# Groups related content

import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

from openai import OpenAI

# Create an Embedding
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']
)

reset_response = client.embeddings.create(
    input="How do I reset my password?",
    model="text-embedding-3-small"
)

print(reset_response.data[0].embedding)

# Compare Two Embeddings
forgotten_login_response = client.embeddings.create(
    input="I forgot my login information",
    model="text-embedding-3-small"
)

print(forgotten_login_response.data[0].embedding)

len(reset_response.data[0].embedding)

len(forgotten_login_response.data[0].embedding)

import numpy as np
from numpy.linalg import norm

# compute cosine similarity
cosine = np.dot(reset_response.data[0].embedding,forgotten_login_response.data[0].embedding)/(norm(reset_response.data[0].embedding)*norm(forgotten_login_response.data[0].embedding)) 
print("Cosine Similarity:", cosine)