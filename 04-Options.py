from dotenv import load_dotenv
import asyncio
import os
from agent_framework.openai import OpenAIResponsesClient

load_dotenv()

async def main():
    agent = OpenAIResponsesClient(api_key=os.getenv("OAI_API_KEY"),
                                  model_id=os.getenv("OAI_MODEL_ID")).as_agent(
        name="Test",
        instructions="Tu es un agent qui écrit un poème sur un thème donné.",
        default_options=
        {
            "temperature": 1.7
        }
    )
    async for chunk in agent.run("Écris un poème sur le thème de l'amitié.", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)

asyncio.run(main())