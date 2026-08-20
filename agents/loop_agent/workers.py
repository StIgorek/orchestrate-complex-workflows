import sys
from pathlib import Path

from google.adk.agents import Agent
from google.adk.tools import ToolContext
from pydantic import BaseModel, Field

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.llm import DEFAULT_MODEL
from tools.search import duckduckgo_search


def exit_loop(tool_context: ToolContext):
    """Викликати ЛИШЕ коли план затверджено — сигналізує про завершення циклу."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    return {}


# Структурований вердикт критика — замінює крихкий string-match на COMPLETION_PHRASE
class PlanCritique(BaseModel):
    is_approved: bool = Field(
        description="True, якщо план вкладається в обмеження (дорога між точками не більше 45 хв)."
    )
    feedback: str = Field(
        description="Якщо is_approved=False — конкретне пояснення, що саме виправити. "
        "Якщо is_approved=True — коротке підтвердження."
    )


# Агент 1: пропонує початковий план
planner_agent = Agent(
    name="planner_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction=(
        "You are a trip planner. Based on the user's request, propose a single "
        "activity and a single restaurant. Output only the names, like: "
        "'Activity: Exploratorium, Restaurant: La Mar'."
    ),
    output_key="current_plan",
)

# Агент 2 (у циклі): досліджує та критикує план у вільній формі (з тулзою)
critic_agent = Agent(
    name="critic_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search],
    instruction="""You are a logistics expert. Your job is to research a travel plan. The user has a strict constraint: total travel time must be short.
    Current Plan: {current_plan}
    Use your tools to check the travel time between the two locations.
    Write a short analysis: state the approximate travel time you found, and whether it is over or under 45 minutes.""",
    output_key="criticism_notes",
)

# Агент 2b (у циклі): перетворює аналіз критика на строгий структурований вердикт (без тулзів)
critic_verdict_agent = Agent(
    name="critic_verdict_agent",
    model=DEFAULT_MODEL,
    output_schema=PlanCritique,
    instruction="""Based on this analysis, produce a structured verdict.
    Analysis: {criticism_notes}
    Set is_approved=true only if the analysis confirms travel time is 45 minutes or under.""",
    output_key="criticism",
)

# Агент 3 (у циклі): доопрацьовує план або виходить із циклу
refiner_agent = Agent(
    name="refiner_agent",
    model=DEFAULT_MODEL,
    tools=[duckduckgo_search, exit_loop],
    instruction="""You are a trip planner, refining a plan based on criticism.
    Original Request: {session.query}
    Critique: {criticism}
    IF criticism.is_approved is true, you MUST call the 'exit_loop' tool.
    ELSE, use criticism.feedback to generate a NEW plan that addresses the issue. Output only the new plan names, like: 'Activity: de Young Museum, Restaurant: Nopa'.""",
    output_key="current_plan",
)
