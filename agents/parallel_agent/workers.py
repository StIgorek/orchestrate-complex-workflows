import sys
from pathlib import Path

from google.adk.agents import Agent

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.llm import DEFAULT_MODEL
from tools.search import duckduckgo_search

museum_finder_agent = Agent(
    name="museum_finder_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction=(
        "You are a museum expert. Find the best museum based on the user's "
        "query. Output only the museum's name."
    ),
    output_key="museum_result",
)

concert_finder_agent = Agent(
    name="concert_finder_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction=(
        "You are an events guide. Find a concert based on the user's query. "
        "Output only the concert name and artist."
    ),
    output_key="concert_result",
)

restaurant_finder_agent = Agent(
    name="restaurant_finder_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction="""You are an expert food critic. Your goal is to find the best restaurant based on a user's request.

    When you recommend a place, you must output *only* the name of the establishment.
    For example, if the best sushi is at 'Jin Sho', you should output only: Jin Sho
    """,
    output_key="restaurant_result",
)

# Агент синтезу результатів
synthesis_agent = Agent(
    name="synthesis_agent",
    model=DEFAULT_MODEL,
    instruction="""You are a helpful assistant. Combine the following research results into a clear, bulleted list for the user.
    - Museum: {museum_result}
    - Concert: {concert_result}
    - Restaurant: {restaurant_result}
    """,
)
