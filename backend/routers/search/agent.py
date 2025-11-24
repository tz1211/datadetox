from typing import List
from agents import Agent, FunctionTool
from .utils import search_huggingface #, search_neo4j

instructions = (
    """
    Receive an input of a model or a dataset.
    Call each tool once:
    - search_neo4j() to get info on connected, similar models / datasets
    - search_huggingface() to get info from HuggingFace.
    Summarize your findings.
    """
)

tools: List[FunctionTool] = [search_huggingface]

search_agent = Agent(
    name="SearchAgent",
    instructions=instructions,
    model="gpt-5-nano",
    tools=tools,
)