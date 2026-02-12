"""Tool for querying RAGFlow knowledge base."""

from langchain_core.tools import tool
from src.services.ragflow import ragflow_service
from src.system.logs import logger

@tool
async def query_knowledge_base(query: str) -> str:
    """Searches the unified knowledge base for information related to the query.
    
    Use this tool whenever you need to find factual information, documentation, 
    or specific domain knowledge that might be stored in the internal knowledge base.
    
    Args:
        query: The search query to look up in the knowledge base.
    """
    logger.info("query_knowledge_base_tool_called", query=query)
    result = await ragflow_service.retrieve(query)
    return result
