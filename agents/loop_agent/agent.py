import sys
from pathlib import Path

from google.adk.agents import LoopAgent, SequentialAgent

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from agents.loop_agent.workers import (
    critic_agent,
    critic_verdict_agent,
    planner_agent,
    refiner_agent,
)

# ✨ LoopAgent: дослідити → винести вердикт → доопрацювати (або вийти) ✨
refinement_loop = LoopAgent(
    name="refinement_loop",
    sub_agents=[critic_agent, critic_verdict_agent, refiner_agent],
    max_iterations=2,
)

# ✨ SequentialAgent об'єднує все разом ✨
iterative_planner_agent = SequentialAgent(
    name="iterative_planner_agent",
    sub_agents=[planner_agent, refinement_loop],
    description="A workflow that iteratively plans and refines a trip to meet constraints.",
)
