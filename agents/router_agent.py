import sys
from pathlib import Path

from google.adk.agents import Agent

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.llm import DEFAULT_MODEL
from agents.sequential_agent.workers import day_trip_agent, foodie_agent
from agents.sequential_agent.agent import find_and_navigate_workflow
from agents.loop_agent.agent import iterative_planner_agent
from agents.parallel_agent.agent import parallel_planner_agent

router_agent = Agent(
    name="router_agent",
    model=DEFAULT_MODEL,
    instruction="""
    You are a master request router. Your job is to analyze a user's query and decide which of the following agents or workflows is best suited to handle it.
    Do not answer the query yourself, only return the name of the most appropriate choice.

    Available Options:
    - 'foodie_agent': For queries *only* about finding a single food place.
    - 'find_and_navigate_agent': For queries that ask to *first find a place* and *then get directions* to it.
    - 'iterative_planner_agent': For planning a trip with a specific constraint that needs checking, like travel time.
    - 'parallel_planner_agent': For queries that ask to find multiple, independent things at once (e.g., a museum AND a concert AND a restaurant).
    - 'day_trip_agent': A general planner for any other simple day trip requests.

    Only return the single, most appropriate option's name and nothing else.
    """,
)

# Словник усіх виконуваних одиниць — і звичайних Agent, і graph-based Workflow.
# workflows.py сам розрізняє їх через isinstance(target, Workflow).
executable_units = {
    "day_trip_agent": day_trip_agent,
    "foodie_agent": foodie_agent,
    "find_and_navigate_agent": find_and_navigate_workflow,
    "iterative_planner_agent": iterative_planner_agent,
    "parallel_planner_agent": parallel_planner_agent,
}
