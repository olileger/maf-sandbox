from dotenv import load_dotenv
import asyncio
import os
from agent_framework.openai import OpenAIResponsesClient
from typing import Annotated

load_dotenv()

def get_weather(location: Annotated[str, "Location to get the weather for"]) -> str:
    """Get the weather for a given location."""
    print("Getting weather...")
    return f"The weather in {location} is sunny with a high of 25°C."

def get_people_count(location: Annotated[str, "Location to get the people count for"]) -> str:
    """Get the people count for a given location."""
    print("Getting people count...")
    return f"There are currently 100 people in {location}."

async def main():
    agent = OpenAIResponsesClient(api_key=os.getenv("OAI_API_KEY"),
                                  model_id=os.getenv("OAI_MODEL_ID")
                                  ).as_agent(
        instructions="You are a helpful assistant providing information about the weather and people count in different locations.",
        tools=[get_weather, get_people_count]
    )

    result = await agent.run("What's the weather like in Paris?")
    print(result)
    
    result = await agent.run("How many people are in New York?")
    print(result)

asyncio.run(main())