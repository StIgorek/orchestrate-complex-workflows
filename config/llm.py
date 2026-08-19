import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

# Використовуємо канонічний клас LiteLlm з ADK, який коректно адаптує параметри виклику
DEFAULT_MODEL = LiteLlm(model=os.getenv("LLM_MODEL", "openai/gpt-5-nano"))
