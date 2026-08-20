import asyncio
import logging
import sys
from agents.workflows import route_and_execute, run_full_app

logging.basicConfig(level=logging.ERROR)


async def main():
    if "--batch" in sys.argv:
        print("🚀 Запуск тестування масиву запитів (--batch)...")
        await run_full_app()
        return

    print("\n🤖 ADK Sequential Workflow Ready.")
    print("Введіть запит для запуску або 'exit' для виходу.\n")

    while True:
        try:
            user_input = input("Prompt > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "вихід"]:
                print("Завершення роботи...")
                break
            await route_and_execute(user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nРоботу перервано.")
            break


if __name__ == "__main__":
    asyncio.run(main())
