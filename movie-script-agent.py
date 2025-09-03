import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

api_key=os.environ['OPENAI_API_KEY'] 

if not api_key:
   raise ValueError("OPENAI_API_KEY not found in local .env file")

from typing import Optional, List
from agents import Agent, Runner, function_tool
from dataclasses import dataclass
import requests
from datetime import datetime
import random

# provides a decorator-based approach to creating classes primarily intended for storing data.
@dataclass
class PlotInfo:
    title: str
    genre: str
    main_character: str
    setting: str
    conflict: str

@function_tool
def generate_plot_twist(plot: str) -> str:
    """Generate a surprise plot twist for a given movie plot."""
    twists = [
        "The protagonist was an AI all along.",
        "The entire journey was just a dream.",
        "The villain turns out to be the hero’s future self.",
        "Earth was a simulation the whole time.",
        "The sidekick is actually the mastermind."
    ]
    twist = random.choice(twists)
    return f"{plot} Plot twist: {twist}"

# Tip: no need for asyncio.run() in notebooks

# Define the movie assistant agent
movie_plot_agent = Agent(
    name="Movie Plot Generator",
    instructions="""
    You are a creative writing assistant who writes movie plots. 
    First, generate the full plot. Then, if the user request mentions a twist or surprise, 
    call the 'generate_plot_twist' function tool using the generated plot as input and 
    use the plot twist to generate an entirely new plot with that twist. 
    Show the user the original plot, alongside the new plot twist.
    Do not add a plot twist if the user doesn't mention one.
    """,
    tools=[generate_plot_twist],
)

async def main():
    runner = Runner()

    with_twist_result = await runner.run(
        movie_plot_agent,
        "Write a sci-fi movie plot with a twist at the end.")
    
    no_twist_result = await runner.run(
        movie_plot_agent,
        "Write a sci-fi movie plot.")
  
    print(with_twist_result.final_output)
    print("-"*70)
    print(no_twist_result.final_output)