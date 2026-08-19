import sys
from pathlib import Path
from google.adk.agents import Agent

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.llm import DEFAULT_MODEL
from tools.search import duckduckgo_search

foodie_agent = Agent(
    name="foodie_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction="""You are an expert food critic. Your goal is to find the best restaurant based on a user's request.

    When you recommend a place, you must output *only* the name of the establishment and nothing else.
    For example, if the best sushi is at 'Jin Sho', you should output only: Jin Sho
    """,
    output_key="destination",
)

transportation_agent = Agent(
    name="transportation_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction="""You are a navigation assistant. Given a destination, provide clear directions.
    The user wants to go to: {destination}.

    Analyze the user's full original query to find their starting point.
    Then, provide clear directions from that starting point to {destination}.
    """,
)

weekend_guide_agent = Agent(
    name="weekend_guide_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction="You are a local events guide. Your task is to find interesting events, concerts, festivals, and activities happening on a specific weekend.",
)

day_trip_agent = Agent(
    name="day_trip_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction="You are the Spontaneous Day Trip Generator. Create full-day itineraries based on mood and budget.",
)
