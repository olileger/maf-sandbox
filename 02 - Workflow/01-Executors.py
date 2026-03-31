import asyncio
from agent_framework import Executor, WorkflowContext, handler, executor, WorkflowBuilder


# Executor as an object
class ExecutorObj(Executor):

    @handler
    async def to_upper_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        """Convert the input to uppercase and forward it to the next node."""
        await ctx.send_message(text.upper())

    @handler
    async def to_lower_case(self, text: str, ctx: WorkflowContext[str]) -> None:
        """Convert the input to lowercase and forward it to the next node."""
        await ctx.send_message(text.lower())


# Executor as a direct function
@executor(id="print_nothing")
async def print_nothing(text: str, ctx: WorkflowContext[str]) -> None:
    """A simple function that does nothing."""
    print("Nothing")


async def main():

    builder = WorkflowBuilder(start_executor=print_nothing)
    workflow = builder.build()


    event = await workflow.run("Hello, World !")
    print(f"Result: {event.get_outputs()}")

asyncio.run(main())