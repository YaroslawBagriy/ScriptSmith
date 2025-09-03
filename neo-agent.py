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

@dataclass
class AsteroidInfo:
    name: str
    is_potentially_hazardous: bool
    estimated_diameter_min_m: float
    estimated_diameter_max_m: float
    close_approach_date: str
    velocity_kmph: float
    miss_distance_km: float
    orbiting_body: str
    jpl_url: str
    
@function_tool
def get_asteroid_data():
    """Fetch near-Earth asteroid data from NASA API for a given date.
    """
    API_KEY = 'DEMO_KEY'
    NASA_BASE_URL = 'https://api.nasa.gov/neo/rest/v1/feed'
   
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        params = {"start_date": today, "end_date": today, "api_key": API_KEY}
        
        #construct request and call api
        response = requests.get(NASA_BASE_URL, params=params)
        data = response.json()

        neos = data["near_earth_objects"].get(today, [])
        if not neos:
            return f"No asteroids are scheduled for close approach on {today}."

        asteroid_report = [f"Near-Earth Asteroids for {today}:"]
        
        for neo in neos:
            approach_data = neo["close_approach_data"][0]
            diameter = neo["estimated_diameter"]["meters"]
            asteroid = AsteroidInfo(
                name=neo["name"],
                is_potentially_hazardous=neo["is_potentially_hazardous_asteroid"],
                estimated_diameter_min_m=diameter["estimated_diameter_min"],
                estimated_diameter_max_m=diameter["estimated_diameter_max"],
                close_approach_date=approach_data["close_approach_date_full"],
                velocity_kmph=float(approach_data["relative_velocity"]["kilometers_per_hour"]),
                miss_distance_km=float(approach_data["miss_distance"]["kilometers"]),
                orbiting_body=approach_data["orbiting_body"],
                jpl_url=neo["nasa_jpl_url"],
            )

            asteroid_report.append(
                f"\n🔹 Name: {asteroid.name}\n"
                f"   - Potentially Hazardous: {'Yes' if asteroid.is_potentially_hazardous else 'No'}\n"
                f"   - Diameter: {asteroid.estimated_diameter_min_m:.1f}–{asteroid.estimated_diameter_max_m:.1f} meters\n"
                f"   - Close Approach: {asteroid.close_approach_date}\n"
                f"   - Speed: {asteroid.velocity_kmph:.2f} km/h\n"
                f"   - Miss Distance: {asteroid.miss_distance_km:.2f} km\n"
                f"   - Orbiting Body: {asteroid.orbiting_body}\n"
                f"   - More Info: {asteroid.jpl_url}"
            )

        return "\n".join(asteroid_report)
    except requests.exceptions.RequestException as e:
        return f"Error fetching asteroid data: {str(e)}"
    
 # Tip: no need for asyncio.run() in notebooks

# Create a NASA Asteroid Tracker assistant
asteroid_assistant = Agent(
   name="Asteroid Tracker",
   instructions="""You are an asteroid tracking assistant that helps users monitor near-Earth asteroids using NASA’s NEO API.

   When asked about asteroid activity, use the get_asteroid_data tool to fetch up-to-date information.
   If the user doesn’t specify a date range, default to the current week (today through 7 days from now).
   Always clarify if the user is interested in only hazardous asteroids or all near-Earth objects.

   Provide summaries that include approach date, asteroid size, speed, distance from Earth, and hazard level.
   Offer helpful insights, like whether an object is unusually close or fast, and reassure the user when appropriate.
   """,
   tools=[get_asteroid_data]
)

async def main():
   runner = Runner()
  
   simple_request = await runner.run(
       asteroid_assistant,
       "What are your capabilities?")
    
   request_with_danger = await runner.run(
       asteroid_assistant, 
       "Is Earth going to be destroyed by an asteroid tonight?")
    
   request_with_count = await runner.run(
       asteroid_assistant, 
       "How many asteroids are headed toward Earth?")

   print(simple_request.final_output)
   print("-"*70)
   print(request_with_danger.final_output)
   print("-"*70)
   print(request_with_count.final_output)
   
