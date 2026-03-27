from dotenv import load_dotenv
import asyncio
import os
from agent_framework.openai import OpenAIResponsesClient
from agent_framework import Agent

load_dotenv()

async def run_stream(agent: Agent, prompt: str):
    # chunk is of type ResponseStream
    async for chunk in agent.run(prompt, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)

async def run(agent: Agent, prompt: str):
    response = await agent.run(prompt)
    # response is of type AgentResponse
    print(response)
    print(response.text) # also works
    i=0
    for m in response.messages:
        print(f"{i}: {m.text}")
        i+=1

async def main():
    client = OpenAIResponsesClient(api_key=os.getenv("OAI_API_KEY"),
                                  model_id=os.getenv("OAI_MODEL_ID"))
    
    await run_stream(client.as_agent(name="Test", instructions="Tu es un agent qui écrit un poème sur un thème donné."), "Écris un poème sur le thème de l'amitié.")
    await run(client.as_agent(name="Test", instructions="Tu es un agent qui écrit un poème sur un thème donné."), "Écris un poème sur le thème de l'amitié.")
    

asyncio.run(main())