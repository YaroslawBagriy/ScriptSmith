
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

from openai import OpenAI

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']  
)

def generate_plot(idea):  
    try:
        completion = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You write movie plots that turn into box office hits. Generate one paragraph."},
                {"role": "user", "content": idea}])
        return completion.choices[0].message.content
    except openai.APIError as e:
      #Handle API error here, e.g. retry or log
      print(f"OpenAI API returned an API Error: {e}")
    
    return "Unable to generate a movie plot due to error. Please try again later."

from IPython.display import Image

def generate_image(movie_plot):  
    try:
        img = client.images.generate(
            model="dall-e-3",
            prompt=movie_plot,
            n=1,
            size="1024x1024"
        ) 

        return img.data[0].url
    except openai.APIError as e:
      #Handle API error here, e.g. retry or log
      print(f"OpenAI API returned an API Error: {e}")
    
    return "Unable to generate an image due to error. Please try again later."

prompt = input("Describe your movie idea: ")

movie_plot = generate_plot(prompt)
print(movie_plot)

image_url = generate_image(movie_plot)
print(image_url)
Image(url=image_url)