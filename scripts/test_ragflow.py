import asyncio
from src.services.ragflow import ragflow_service
from src.agent.tools.ragflow_retriever import query_knowledge_base
from src.config.settings import settings

async def test_ragflow():
    print(f"RAGFlow Base URL: {settings.RAGFLOW_BASE_URL}")
    print(f"RAGFlow Chat ID: {settings.RAGFLOW_CHAT_ID}")
    print(f"RAGFlow API Key set: {bool(settings.RAGFLOW_API_KEY)}")
    
    query = "What is the capital of France?"
    print(f"\nTesting RAGFlowService.retrieve with query: '{query}'")
    # Result will likely be a warning/error message if keys are dummy
    result = await ragflow_service.retrieve(query)
    print(f"Result: {result}")
    
    print(f"\nTesting query_knowledge_base tool with query: '{query}'")
    tool_result = await query_knowledge_base.ainvoke({"query": query})
    print(f"Tool Result: {tool_result}")

if __name__ == "__main__":
    asyncio.run(test_ragflow())
