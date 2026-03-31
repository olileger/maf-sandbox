import asyncio
from dotenv import load_dotenv
import os
from agent_framework import AgentResponseUpdate, WorkflowBuilder, Executor, handler, AgentExecutorResponse, WorkflowContext
from agent_framework.openai import OpenAIResponsesClient
from typing_extensions import Never

# Fan-in: besoin d'un objet ou fonction qui agrège les résultats de plusieurs agents.
# Ici, on va juste concaténer les réponses des agents pour les afficher dans une seule réponse finale.
class Answer(Executor):
    @handler
    async def aggregate(self, results: list[AgentExecutorResponse], ctx: WorkflowContext[Never, str]) -> None:
        # Map responses to text by executor id for a simple, predictable demo.
        by_id: dict[str, str] = {}
        for r in results:
            # AgentExecutorResponse.agent_response.text is the assistant text produced by the agent.
            by_id[r.executor_id] = r.agent_response.text

        res = "Aggregated results:\n"
        for id, text in by_id.items():
            res += f"\n{id}:\n{text}\n"
        await ctx.yield_output(res)

    
async def main():
    client = OpenAIResponsesClient(api_key=os.getenv("OAI_API_KEY"),
                                   model_id=os.getenv("OAI_MODEL_ID"))

    imagineur = client.as_agent(name="Imagineur",
                                instructions="Tu es un agent qui imagine un thème selon un mot clé donné.")
    writer1 = client.as_agent(name="Writer1",
                             instructions="Tu es un agent qui écrit un poème sur un thème donné en étant neutre.")
    writer2 = client.as_agent(name="Writer2",
                             instructions="Tu es un agent qui écrit un poème sur un thème donné en étant très fantaisiste.")
    writer3 = client.as_agent(name="Writer3",
                             instructions="Tu es un agent qui écrit un poème sur un thème donné en étant très solennel.")
    reviewer = client.as_agent(name="Reviewer",
                               instructions="Tu es un agent qui donne des conseils à un poete pour améliorer son poème. Sois constructif et précis.")


    # Fan Out / Fan In: plusieurs agents écrivent un poème, puis on aggrège les résultats pour les afficher dans une seule réponse finale.
    builder = WorkflowBuilder(start_executor=imagineur)
    builder.add_fan_out_edges(imagineur, [writer1, writer2, writer3])
    builder.add_fan_in_edges([writer1, writer2, writer3], Answer(id="answer"))
    wf = builder.build()

    events = await wf.run("amitié")
    print(f"Final result: {events.get_outputs()}")

asyncio.run(main())