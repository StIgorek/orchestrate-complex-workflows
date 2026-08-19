import sys
from pathlib import Path
from google.adk.agents import Agent

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.llm import DEFAULT_MODEL
from tools.search import duckduckgo_search

day_trip_agent = Agent(
    name="day_trip_agent",
    model=DEFAULT_MODEL,
    description="Generates spontaneous full-day itineraries based on mood and budget.",
    instruction="""
    You are the Spontaneous Day Trip Generator 🚗.
    Create full-day itineraries (morning, afternoon, evening) using real-time information.
    Format your response in Markdown with clear time blocks.
    """,
    tools=[duckduckgo_search],
)

foodie_agent = Agent(
    name="foodie_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction=" You are an expert food critic. Find the absolute best food experiences. State venue names clearly in bold, e.g., 'The best sushi is at **Jin Sho**.'",
)

weekend_guide_agent = Agent(
    name="weekend_guide_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction="You are a local events guide. Find events, concerts, and activities for a specific weekend.",
)

transportation_agent = Agent(
    name="transportation_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction="You are a navigation assistant. Provide precise directions between specified locations.",
)

router_agent = Agent(
    name="router_agent",
    model=DEFAULT_MODEL,
    instruction="""
    Analyze the user's query and decide which worker agent or workflow to use.
    Do not answer the query directly. Return ONLY one option name from:
    - 'foodie_agent'
    - 'weekend_guide_agent'
    - 'day_trip_agent'
    - 'find_and_navigate_combo'

    Do not include quotes or extra text in your output.
    """,
)

worker_agents = {
    "day_trip_agent": day_trip_agent,
    "foodie_agent": foodie_agent,
    "weekend_guide_agent": weekend_guide_agent,
    "transportation_agent": transportation_agent,
}
