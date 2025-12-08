import json
from agents import RunResultStreaming, Runner
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from openai.types.responses import ResponseTextDeltaEvent
from pydantic import BaseModel

import logging
from rich.logging import RichHandler

from .search import compiler_agent, hf_search_agent, neo4j_search_agent
from .search.utils.tool_state import get_tool_result, set_request_context

router = APIRouter(prefix="/flow")

logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])
logger = logging.getLogger(__name__)


class Query(BaseModel):
    query_val: str


async def stream_search_results(query_val: str, request: Request):
    """Async generator that streams search results as Server-Sent Events"""
    search_logger = logger.getChild("search")
    request.state.tool_results = {}
    request.state.original_query = query_val
    set_request_context(request)

    search_logger.info(f"Query '{query_val}' is running.")

    ### HF
    try:
        hf_result: RunResultStreaming = Runner.run_streamed(
            starting_agent=hf_search_agent, input=query_val
        )
        async for event in hf_result.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                yield f"data: {json.dumps({'type': 'delta', 'content': event.data.delta})}\n\n"

        hf_final = hf_result.final_output_as(str)

    except Exception as e:
        search_logger.error(f"Failed to run HF search: {e}")
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        return

    ### NEO4J
    try:
        neo4j_result: RunResultStreaming = Runner.run_streamed(
            starting_agent=neo4j_search_agent, input=hf_final
        )
        async for event in neo4j_result.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                yield f"data: {json.dumps({'type': 'delta', 'content': event.data.delta})}\n\n"

    except Exception as e:
        search_logger.error(f"Failed to run Neo4j search: {e}")
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        return

    ### Get Neo4j graph data from tool results
    neo4j_data = get_tool_result("search_neo4j", request)

    ### FINAL COMPILER
    try:
        compiled_response: RunResultStreaming = Runner.run_streamed(
            starting_agent=compiler_agent, input=query_val
        )
        async for event in compiled_response.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                yield f"data: {json.dumps({'type': 'delta', 'content': event.data.delta})}\n\n"

        final_result = compiled_response.final_output_as(str)

    except Exception as e:
        search_logger.error(f"Failed to run compiler: {e}")
        yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"
        return

    # Send final result with neo4j_data
    final_response = {"type": "complete", "result": final_result}
    if neo4j_data is not None:
        final_response["neo4j_data"] = neo4j_data.model_dump()

    yield f"data: {json.dumps(final_response)}\n\n"


@router.post("/search")
async def run_search(query: Query, request: Request):
    return StreamingResponse(
        stream_search_results(query.query_val, request), media_type="text/event-stream"
    )
