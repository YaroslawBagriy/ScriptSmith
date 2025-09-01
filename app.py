import openai
import os
from openai import OpenAI

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']  
)