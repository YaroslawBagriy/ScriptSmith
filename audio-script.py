import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

from openai import OpenAI

# Create OpenAI client with the given OPENAI_API_KEY
# from the environment variables
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']  
)

from pathlib import Path

speech_file_path = os.path.dirname(os.path.abspath("__file__"))+"/" +"speech.mp3"
with client.audio.speech.with_streaming_response.create(
  model="gpt-4o-mini-tts",
  voice="alloy", #voices: alloy ash ballad coral echo fable nova onyx sage shimmer
  input="Welcome to your AI-powered app. Let's get started!"
) as response:
  response.stream_to_file(speech_file_path)

from IPython.display import Audio
Audio("speech.mp3")