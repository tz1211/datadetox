import os
import json
import asyncio
import logging
from dotenv import load_dotenv
from typing import Any, AsyncIterator, Dict, List, Sequence

from openai import OpenAI

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse, PlainTextResponse
from pydantic import BaseModel

# from agents import (
#     Agent,
#     InputGuardrailTripwireTriggered,
#     Runner,
#     RunResult,
#     RunResultStreaming,
#     TResponseInputItem,
#     custom_span,
#     trace,
# )
# from agents.extensions.visualization import draw_graph
# from agents.items import ItemHelpers
# from agents.mcp import MCPServerSse
# from context import ShinanContext
# from openai.types.responses import (
#     ResponseTextDeltaEvent,
# )

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)

router = APIRouter(prefix="/datadetox", tags=["client"])

@router.post("/query") 
async def query_hf(request: Request): 
    # initialise openai client
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    # some eclair MCP magic 
    pass 