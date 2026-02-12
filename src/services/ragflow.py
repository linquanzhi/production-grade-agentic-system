"""RAGFlow service for integrating with external RAG knowledge base."""

import httpx
from typing import Any, Dict, List, Optional
from src.config.settings import settings
from src.system.logs import logger

class RAGFlowService:
    """Service for interacting with RAGFlow API."""

    def __init__(self):
        self.base_url = settings.RAGFLOW_BASE_URL.rstrip("/")
        self.api_key = settings.RAGFLOW_API_KEY
        self.chat_id = settings.RAGFLOW_CHAT_ID
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def retrieve(self, query: str) -> str:
        """Retrieve relevant information from RAGFlow knowledge base.

        Args:
            query: The search query

        Returns:
            str: The retrieved content with references if available
        """
        if not self.api_key or not self.chat_id:
            logger.warning("ragflow_not_configured", api_key_set=bool(self.api_key), chat_id_set=bool(self.chat_id))
            return "RAGFlow is not configured. Please provide API key and Chat ID."

        url = f"{self.base_url}/chats_openai/{self.chat_id}/chat/completions"
        
        # Following RAGFlow OpenAI-compatible API format
        payload = {
            "model": "ragflow", # RAGFlow usually expects this or specific internal model name
            "messages": [
                {"role": "user", "content": query}
            ],
            "stream": False
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # Extract content from response
                choices = data.get("choices", [])
                if not choices:
                    return "No response from RAGFlow."
                
                content = choices[0].get("message", {}).get("content", "")
                
                # RAGFlow often includes references in 'extra_body' or similar
                # depending on specific API version/config
                logger.info("ragflow_retrieval_successful", query=query)
                return content

        except httpx.HTTPStatusError as e:
            logger.error("ragflow_api_error", status_code=e.response.status_code, error=str(e))
            return f"Error communicating with RAGFlow: {str(e)}"
        except Exception as e:
            logger.error("ragflow_unexpected_error", error=str(e))
            return f"An unexpected error occurred while querying RAGFlow: {str(e)}"

# Singleton instance
ragflow_service = RAGFlowService()
