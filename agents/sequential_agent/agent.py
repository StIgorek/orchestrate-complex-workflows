import sys
from pathlib import Path
from google.adk.agents import Agent
from google.adk import Workflow

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.llm import DEFAULT_MODEL
from agents.sequential_agent.workers import (
    foodie_agent,
    transportation_agent,
    weekend_guide_agent,
    day_trip_agent,
)

find_and_navigate_workflow = Workflow(
    name="find_and_navigate_agent",
    description="A workflow that first finds a location and then provides directions to it.",
    edges=[
        ("START", foodie_agent, transportation_agent),
    ],
)

router_agent = Agent(
    name="router_agent",
    model=DEFAULT_MODEL,
    instruction="""
    You are a request router. Analyze the query and select the appropriate execution path.
    Do not answer directly. Return ONLY the exact name of the selected target.

    Available Options:
    - 'foodie_agent'
    - 'weekend_guide_agent'
    - 'day_trip_agent'
    - 'find_and_navigate_agent'
    """,
)

executable_units = {
    "day_trip_agent": day_trip_agent,
    "foodie_agent": foodie_agent,
    "weekend_guide_agent": weekend_guide_agent,
    "find_and_navigate_agent": find_and_navigate_workflow,
}
