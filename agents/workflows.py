import logging
import sys
from pathlib import Path
from google.adk import Workflow, Runner
from google.genai.types import Content, Part

sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.base_runner import create_agent_session, run_agent_query, session_service
from agents.sequential_agent.agent import router_agent, executable_units

logger = logging.getLogger("ADK_Workflows")


async def route_and_execute(query: str) -> None:
    print(f"\n{'='*60}\n🗣️ Processing Query: '{query}'\n{'='*60}")

    router_session = await create_agent_session(app_name=router_agent.name)
    raw_route = await run_agent_query(
        agent=router_agent, query=query, session=router_session, is_router=True
    )
    chosen_route = raw_route.strip().replace("'", "").replace('"', "")
    print(f"🚦 Router selected route: '{chosen_route}'")

    if chosen_route not in executable_units:
        print(f"🚨 Error: Unknown route '{chosen_route}'")
        return

    target = executable_units[chosen_route]

    if isinstance(target, Workflow):
        print(f"\n🚀 Running Graph Workflow: '{target.name}'")
        session = await create_agent_session(app_name=target.name)
        runner = Runner(
            agent=target, session_service=session_service, app_name=target.name
        )
        user_message = Content(parts=[Part(text=query)], role="user")

        user_id = getattr(session, "user_id", "default_user")

        async for event in runner.run_async(
            user_id=user_id, session_id=session.id, new_message=user_message
        ):
            if hasattr(event, "content") and event.content and event.content.parts:
                print(f"📌 Step Output: {event.content.parts[0].text}")
            elif hasattr(event, "text") and event.text:
                print(f"📌 Step Output: {event.text}")
    else:
        session = await create_agent_session(app_name=target.name)
        await run_agent_query(target, query, session)


async def run_sequential_app() -> None:
    queries = [
        "I want to eat the best sushi in Palo Alto.",
        "Are there any cool outdoor concerts this weekend?",
        "Find me the best sushi in Palo Alto and then tell me how to get there from the Caltrain station.",
    ]
    for query in queries:
        await route_and_execute(query)
