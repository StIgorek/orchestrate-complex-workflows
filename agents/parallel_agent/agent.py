import logging

from google.adk.agents import ParallelAgent, SequentialAgent

from agents.parallel_agent.workers import (
    concert_finder_agent,
    museum_finder_agent,
    restaurant_finder_agent,
    synthesis_agent,
)

logger = logging.getLogger("ParallelAgent")

# ✨ ParallelAgent запускає трьох спеціалістів одночасно ✨
parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    sub_agents=[museum_finder_agent, concert_finder_agent, restaurant_finder_agent],
)

# ✨ SequentialAgent: спершу паралельний пошук, потім синтез ✨
parallel_planner_agent = SequentialAgent(
    name="parallel_planner_agent",
    sub_agents=[parallel_research_agent, synthesis_agent],
    description="A workflow that finds multiple things in parallel and then summarizes the results.",
)

logger.info("🤖 Agent team supercharged with a ParallelAgent workflow!")
