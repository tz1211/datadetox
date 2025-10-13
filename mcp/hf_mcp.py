import os
import logging
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from fastmcp import FastMCP
from huggingface_hub import HfApi, ModelInfo, DatasetInfo, SpaceInfo

load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

HOST = os.getenv("HF_MCP_HOST", "0.0.0.0")
PORT = int(os.getenv("HF_MCP_PORT", "8080"))
HF_TOKEN = os.getenv("HF_TOKEN", None)

api = HfApi(token=HF_TOKEN)

def create_server():
    mcp = FastMCP(
        name="HuggingFace MCP",
        instructions="""
This server provides tools to search Hugging Face Hub and retrieve repo cards.
Tools:
- hf_search(query, kind, limit, filter)
- hf_card(repo_id, kind)
"""
    )

    @mcp.tool()
    async def hf_search(
        query: str,
        kind: str = "models",  # "models" | "datasets" | "spaces"
        limit: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, List[Dict[str, Any]]]:
        if not query or not query.strip():
            return {"results": []}
        filter = filter or {}
        results: List[Dict[str, Any]] = []

        if kind == "models":
            for m in api.list_models(search=query, limit=limit, **filter):
                assert isinstance(m, ModelInfo)
                results.append({
                    "repo_id": m.modelId,
                    "author": m.author,
                    "sha": m.sha,
                    "likes": m.likes,
                    "downloads": m.downloads,
                    "tags": m.tags,
                    "private": m.private,
                    "library_name": getattr(m, "library_name", None),
                    "url": f"https://huggingface.co/{m.modelId}",
                    "kind": "model",
                })
        elif kind == "datasets":
            for d in api.list_datasets(search=query, limit=limit, **filter):
                assert isinstance(d, DatasetInfo)
                results.append({
                    "repo_id": d.id,
                    "author": d.author,
                    "sha": d.sha,
                    "likes": d.likes,
                    "downloads": d.downloads,
                    "tags": d.tags,
                    "private": d.private,
                    "url": f"https://huggingface.co/datasets/{d.id}",
                    "kind": "dataset",
                })
        elif kind == "spaces":
            for s in api.list_spaces(search=query, limit=limit, **filter):
                assert isinstance(s, SpaceInfo)
                results.append({
                    "repo_id": s.id,
                    "author": s.author,
                    "sha": s.sha,
                    "likes": s.likes,
                    "tags": s.tags,
                    "private": s.private,
                    "runtime": s.runtime,
                    "sdk": s.sdk,
                    "url": f"https://huggingface.co/spaces/{s.id}",
                    "kind": "space",
                })
        else:
            raise ValueError("kind must be one of: models, datasets, spaces")

        return {"results": results}

    @mcp.tool()
    async def hf_card(repo_id: str, kind: str = "model") -> Dict[str, Any]:
        if not repo_id:
            raise ValueError("repo_id required")
        kind = kind.lower()
        if kind == "model":
            card = api.model_info(repo_id)
            readme = api.model_card(repo_id).text if hasattr(api, "model_card") else None
            url = f"https://huggingface.co/{repo_id}"
        elif kind == "dataset":
            card = api.dataset_info(repo_id)
            readme = api.dataset_card(repo_id).text if hasattr(api, "dataset_card") else None
            url = f"https://huggingface.co/datasets/{repo_id}"
        elif kind == "space":
            card = api.space_info(repo_id)
            readme = None
            url = f"https://huggingface.co/spaces/{repo_id}"
        else:
            raise ValueError("kind must be model|dataset|space")

        return {
            "repo_id": repo_id,
            "kind": kind,
            "url": url,
            "card": card.__dict__ if hasattr(card, "__dict__") else card,
            "readme": readme,
        }

    return mcp

def main():
    server = create_server()
    logger.info(f"Starting HF MCP on {HOST}:{PORT} (SSE)")
    server.run(transport="sse", host=HOST, port=PORT)

if __name__ == "__main__":
    main()