import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

from openai import OpenAI

#client = OpenAI(api_key=YOUR_API_KEY)
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']  
)

from IPython.display import Image

img = client.images.generate(
    model="dall-e-3",
    prompt="A futuristic city skyline at sunset, digital art style",
    n=1,
    size="1024x1024"
)

image_url = img.data[0].url

print(image_url)

Image(url=image_url)

img = client.images.generate(
    model="dall-e-3", #Model you want to use.
    prompt="A minimalist logo for a tech startup called CloudNest, black and white", #Your description of the image
    n=1, #Number of images to generate
    size="1024x1024" #Image size
)

image_url = img.data[0].url #URL that points to the generated image hosted by OpenAI

print(image_url)

Image(url=image_url)

try:
    img = client.images.generate(
        model="dall-e-3", #Model you want to use.
        prompt="", #Your description of the image
        n=1, #Number of images to generate
        size="1024x1024" #Image size
    )
except openai.APIError as e:
  #Handle API error here, e.g. retry or log
  print(f"OpenAI API returned an API Error: {e}")
  pass

# Image reasoning section

import base64

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Path to your image
image_path = "cars_sold.png"

# Getting the Base64 string
base64_image = encode_image(image_path)

completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "Summarize the data shown in this bar chart." },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
)

print(completion.choices[0].message.content)

completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "Based on the chart in this image, which month had the greatest increase and why might that be?" },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ],
)

print(completion.choices[0].message.content)