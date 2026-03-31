import asyncio
from dotenv import load_dotenv
import os
from agent_framework import AgentResponseUpdate, WorkflowBuilder
from agent_framework.openai import OpenAIResponsesClient


async def main():
    client = OpenAIResponsesClient(api_key=os.getenv("OAI_API_KEY"),
                                   model_id=os.getenv("OAI_MODEL_ID"))

    writer = client.as_agent(name="Writer",
                             instructions="Tu es un agent qui écrit un poème sur un thème donné.")
    reviewer = client.as_agent(name="Reviewer",
                               instructions="Tu es un agent qui donne des conseils à un poete pour améliorer son poème. Sois constructif et précis.")

    builder = WorkflowBuilder(start_executor=writer)
    builder.add_edge(writer, reviewer)
    wf = builder.build()

    events = wf.run("Écris un poème sur le thème de l'amitié.", stream=True)
    async for e in events:
        if e.type == "output" and isinstance(e.data, AgentResponseUpdate):
            update = e.data
            print(f"Update from: {update.author_name}: {update.text}\n", end="", flush=True)

asyncio.run(main())