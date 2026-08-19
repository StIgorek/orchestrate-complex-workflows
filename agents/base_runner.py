import logging
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai.types import Content, Part

logger = logging.getLogger("ADK_Runner")

session_service = InMemorySessionService()
MY_USER_ID = "adk_orchestrator_user_001"


async def create_agent_session(app_name: str, user_id: str = MY_USER_ID) -> Session:
    """Створює та повертає сесію, прив'язану до імені застосунку."""
    return await session_service.create_session(app_name=app_name, user_id=user_id)


async def run_agent_query(
    agent: Agent,
    query: str,
    session: Session,
    user_id: str = MY_USER_ID,
    is_router: bool = False,
) -> str:
    """Виконує запит до агента з обробкою подій за стандартом ADK."""
    if not is_router:
        print(f"\n🚀 Виконання агента: '{agent.name}' | Сесія: '{session.id}'")

    runner = Runner(agent=agent, session_service=session_service, app_name=agent.name)

    final_response = ""
    try:
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=Content(parts=[Part(text=query)], role="user"),
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text
                else:
                    final_response = getattr(
                        event, "text", "⚠️ Модель не повернула текст."
                    )
    except Exception as e:
        logger.error(f"Execution error in agent '{agent.name}': {e}", exc_info=True)
        final_response = f"An error occurred: {str(e)}"

    if not is_router:
        print("\n" + "-" * 50)
        print("✅ Фінальна відповідь:")
        print(final_response)
        print("-" * 50 + "\n")

    return final_response
