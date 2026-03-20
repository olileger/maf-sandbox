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
    )
    result = await agent.run("Écris un poème sur le thème de l'amitié.")
    print(result)

asyncio.run(main())