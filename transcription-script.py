import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

from openai import OpenAI

#client = OpenAI(api_key=YOUR_API_KEY)
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']  
)

from pathlib import Path

# Upload and transcribe audio file
speech_file_path = os.path.dirname(os.path.abspath("__file__"))+"/" +"speech.mp3"
audio_file= open(speech_file_path, "rb")

transcription = client.audio.transcriptions.create(
    model="gpt-4o-transcribe", 
    file=audio_file
)

print(transcription.text)

# Upload and transcribe audio file with different language
speech_file_path = os.path.dirname(os.path.abspath("__file__"))+"/" +"LinkedIn-Learning-IT.m4a"
audio_file= open(speech_file_path, "rb")

transcription = client.audio.transcriptions.create(
    model="gpt-4o-transcribe", 
    file=audio_file
)

print(transcription.text)