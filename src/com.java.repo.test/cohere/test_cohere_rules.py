#!/usr/bin/env python3
"""
Test file for Cohere LLM Semgrep rules validation.
This file contains various Cohere SDK usage patterns that should be detected by the rules.
"""

import os
import asyncio
from typing import List, Dict, Any

# Rule 1: Cohere SDK imports
import cohere
from cohere import Client, AsyncClient, ClientV2, AsyncClientV2
from cohere.client import Client as CohereClient
from cohere.client import AsyncClient as CohereAsyncClient
from cohere.client import ClientV2 as CohereClientV2
from cohere.client import AsyncClientV2 as CohereAsyncClientV2
import cohere as co

# Rule 2: Cohere Compass SDK imports
import cohere_compass
from cohere_compass import CompassClient, AsyncCompassClient
from cohere_compass.client import CompassClient as CompassClientAlias
from cohere_compass.client import AsyncCompassClient as AsyncCompassClientAlias
import cohere_compass as compass

# Rule 3: Cohere API Client instantiation
client = cohere.Client(api_key="co-123456789abcdef")
client_v2 = cohere.ClientV2(api_key="co-123456789abcdef")
async_client = cohere.AsyncClient(api_key="co-123456789abcdef")
async_client_v2 = cohere.AsyncClientV2(api_key="co-123456789abcdef")

# Alternative client instantiation
client_alt = cohere.Client()
client_v2_alt = cohere.ClientV2()
async_client_alt = cohere.AsyncClient()
async_client_v2_alt = cohere.AsyncClientV2()

# Rule 4: Cohere Compass Client instantiation
compass_client = cohere_compass.CompassClient(api_key="co-123456789abcdef")
compass_async_client = cohere_compass.AsyncCompassClient(api_key="co-123456789abcdef")

# Rule 13: API key usage patterns
key_client = cohere.Client(api_key="co-123456789abcdef")
key_client_v2 = cohere.ClientV2(api_key="co-123456789abcdef")
key_async_client = cohere.AsyncClient(api_key="co-123456789abcdef")
key_async_client_v2 = cohere.AsyncClientV2(api_key="co-123456789abcdef")
key_compass_client = cohere_compass.CompassClient(api_key="co-123456789abcdef")
key_compass_async_client = cohere_compass.AsyncCompassClient(api_key="co-123456789abcdef")

# Rule 14: Environment variable usage
api_key_env = os.environ.get("COHERE_API_KEY")
api_key_env_alt = os.getenv("COHERE_API_KEY")
api_key_env_direct = os.environ["COHERE_API_KEY"]
api_key_co = os.environ.get("CO_API_KEY")
api_key_co_alt = os.getenv("CO_API_KEY")
api_key_co_direct = os.environ["CO_API_KEY"]

def test_chat_api():
    """Rule 5: Chat API calls"""
    client = cohere.Client(api_key="co-123456789abcdef")
    
    # Basic chat
    response = client.chat(
        model="command-r",
        message="Hello, how are you?"
    )
    
    # Chat stream
    stream_response = client.chat_stream(
        model="command-r-plus",
        message="Tell me a story"
    )
    
    # V2 chat
    client_v2 = cohere.ClientV2(api_key="co-123456789abcdef")
    v2_response = client_v2.v2.chat(
        model="command-r-08-2024",
        messages=[{"role": "user", "content": "Hello"}]
    )

def test_generate_api():
    """Rule 6: Generate API calls"""
    client = cohere.Client(api_key="co-123456789abcdef")
    
    # Basic generation
    response = client.generate(
        model="command-r",
        prompt="Once upon a time"
    )
    
    # Generate stream
    stream_response = client.generate_stream(
        model="command-r-plus",
        prompt="Write a story about AI"
    )

def test_embed_api():
    """Rule 7: Embeddings API calls"""
    client = cohere.Client(api_key="co-123456789abcdef")
    
    # Basic embedding
    response = client.embed(
        model="embed-english-v3.0",
        texts=["Hello world", "How are you?"]
    )
    
    # V2 embedding
    client_v2 = cohere.ClientV2(api_key="co-123456789abcdef")
    v2_response = client_v2.v2.embed(
        model="embed-multilingual-v3.0",
        texts=["Hello", "Hola", "Bonjour"]
    )

def test_rerank_api():
    """Rule 8: Rerank API calls"""
    client = cohere.Client(api_key="co-123456789abcdef")
    
    documents = [
        {"text": "Carson City is the capital city of Nevada."},
        {"text": "The Commonwealth of the Northern Mariana Islands is a group of islands."},
        {"text": "Washington, D.C. is the capital of the United States."}
    ]
    
    # Basic rerank
    response = client.rerank(
        model="rerank-english-v3.0",
        query="What is the capital of the United States?",
        documents=documents
    )
    
    # V2 rerank
    client_v2 = cohere.ClientV2(api_key="co-123456789abcdef")
    v2_response = client_v2.v2.rerank(
        model="rerank-multilingual-v3.0",
        query="US capital",
        documents=documents
    )

def test_compass_api():
    """Rule 9: Compass API calls"""
    compass_client = cohere_compass.CompassClient(api_key="co-123456789abcdef")
    
    # Search
    search_response = compass_client.search(
        query="AI technologies",
        index_name="my_index"
    )
    
    # Index documents
    index_response = compass_client.index(
        index_name="my_index",
        documents=[{"text": "AI is transforming the world"}]
    )
    
    # Create index
    create_response = compass_client.create_index(
        index_name="new_index",
        dimension=1024
    )
    
    # Delete index
    delete_response = compass_client.delete_index(
        index_name="old_index"
    )
    
    # List indexes
    list_response = compass_client.list_indexes()

def test_model_usage():
    """Rule 10: Model usage patterns"""
    client = cohere.Client(api_key="co-123456789abcdef")
    
    # Command models
    client.chat(model="command-r")
    client.chat(model="command-r-plus")
    client.chat(model="command-r-08-2024")
    client.chat(model="command-r-plus-08-2024")
    client.chat(model="c4ai-aya-23-35b")
    client.chat(model="c4ai-aya-23-8b")
    
    # Embed models
    client.embed(model="embed-english-v3.0")
    client.embed(model="embed-multilingual-v3.0")
    
    # Rerank models
    client.rerank(model="rerank-english-v3.0")
    client.rerank(model="rerank-multilingual-v3.0")

def test_streaming():
    """Rule 11: Streaming patterns"""
    client = cohere.Client(api_key="co-123456789abcdef")
    
    # Chat stream
    stream = client.chat_stream(
        model="command-r",
        message="Tell me a joke"
    )
    
    # Generate stream
    gen_stream = client.generate_stream(
        model="command-r",
        prompt="Write a poem"
    )
    
    # Stream iteration
    for event in client.chat_stream(model="command-r", message="Hello"):
        print(event)

def test_tool_calling():
    """Rule 12: Tool/function calling"""
    client = cohere.Client(api_key="co-123456789abcdef")
    
    tools = [
        {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                }
            }
        }
    ]
    
    # Chat with tools
    response = client.chat(
        model="command-r",
        message="What's the weather like?",
        tools=tools
    )
    
    # V2 chat with tools
    client_v2 = cohere.ClientV2(api_key="co-123456789abcdef")
    v2_response = client_v2.v2.chat(
        model="command-r-plus",
        messages=[{"role": "user", "content": "What's the weather?"}],
        tools=tools
    )

async def test_async_patterns():
    """Rule 15: Async patterns"""
    async_client = cohere.AsyncClient(api_key="co-123456789abcdef")
    
    # Async chat
    response = await async_client.chat(
        model="command-r",
        message="Hello async world"
    )
    
    # Async generate
    gen_response = await async_client.generate(
        model="command-r",
        prompt="Async generation test"
    )
    
    # Async embed
    embed_response = await async_client.embed(
        model="embed-english-v3.0",
        texts=["async embedding test"]
    )
    
    # Async rerank
    rerank_response = await async_client.rerank(
        model="rerank-english-v3.0",
        query="async query",
        documents=[{"text": "async document"}]
    )
    
    # Async chat stream
    stream_response = await async_client.chat_stream(
        model="command-r",
        message="Async stream test"
    )
    
    # Async generate stream
    gen_stream_response = await async_client.generate_stream(
        model="command-r",
        prompt="Async generate stream test"
    )
    
    # V2 async patterns
    async_client_v2 = cohere.AsyncClientV2(api_key="co-123456789abcdef")
    v2_chat_response = await async_client_v2.v2.chat(
        model="command-r-plus",
        messages=[{"role": "user", "content": "V2 async test"}]
    )
    
    v2_embed_response = await async_client_v2.v2.embed(
        model="embed-multilingual-v3.0",
        texts=["V2 async embedding"]
    )
    
    v2_rerank_response = await async_client_v2.v2.rerank(
        model="rerank-multilingual-v3.0",
        query="V2 async rerank",
        documents=[{"text": "V2 async document"}]
    )

async def test_compass_async():
    """Rule 9 & 15: Compass async patterns"""
    compass_async_client = cohere_compass.AsyncCompassClient(api_key="co-123456789abcdef")
    
    # Async search
    search_response = await compass_async_client.search(
        query="AI technologies",
        index_name="my_index"
    )
    
    # Async index
    index_response = await compass_async_client.index(
        index_name="my_index",
        documents=[{"text": "AI is transforming the world"}]
    )
    
    # Async create index
    create_response = await compass_async_client.create_index(
        index_name="new_index",
        dimension=1024
    )
    
    # Async delete index
    delete_response = await compass_async_client.delete_index(
        index_name="old_index"
    )
    
    # Async list indexes
    list_response = await compass_async_client.list_indexes()

async def test_async_streaming():
    """Rule 11 & 15: Async streaming patterns"""
    async_client = cohere.AsyncClient(api_key="co-123456789abcdef")
    
    # Async for loop with chat stream
    async for event in async_client.chat_stream(model="command-r", message="Hello"):
        print(event)
    
    # Async for loop with generate stream
    async for token in async_client.generate_stream(model="command-r", prompt="Hello"):
        print(token)

async def test_async_tool_calling():
    """Rule 12 & 15: Async tool calling"""
    async_client = cohere.AsyncClient(api_key="co-123456789abcdef")
    
    tools = [
        {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                }
            }
        }
    ]
    
    # Async chat with tools
    response = await async_client.chat(
        model="command-r",
        message="What's the weather like?",
        tools=tools
    )
    
    # Async V2 chat with tools
    async_client_v2 = cohere.AsyncClientV2(api_key="co-123456789abcdef")
    v2_response = await async_client_v2.v2.chat(
        model="command-r-plus",
        messages=[{"role": "user", "content": "What's the weather?"}],
        tools=tools
    )

async def test_async_functions():
    """Rule 15: Async function patterns"""
    async def process_chat():
        client = cohere.AsyncClient(api_key="co-123456789abcdef")
        result = await client.chat(
            model="command-r",
            message="Hello from async function"
        )
        return result
    
    async def process_generate():
        client = cohere.AsyncClient(api_key="co-123456789abcdef")
        result = await client.generate(
            model="command-r",
            prompt="Generate from async function"
        )
        return result
    
    async def process_compass_search():
        client = cohere_compass.AsyncCompassClient(api_key="co-123456789abcdef")
        result = await client.search(
            query="Search from async function",
            index_name="my_index"
        )
        return result
    
    # Call the async functions
    chat_result = await process_chat()
    generate_result = await process_generate()
    search_result = await process_compass_search()

# Test functions that should NOT be detected (non-Cohere patterns)
def test_non_cohere_patterns():
    """These patterns should NOT trigger any Cohere rules"""
    
    # Generic client patterns (should not match)
    generic_client = SomeOtherClient()
    generic_client.chat(message="Hello")
    generic_client.generate(prompt="Test")
    generic_client.embed(texts=["Test"])
    
    # Generic async patterns (should not match)
    async def generic_async():
        client = SomeOtherAsyncClient()
        await client.chat(message="Hello")
        await client.generate(prompt="Test")
    
    # Generic model usage (should not match)
    other_model = "gpt-4"
    another_model = "claude-3"
    
    # Generic streaming (should not match)
    for event in some_other_client.stream():
        pass
    
    # Generic tool calling (should not match)
    other_client.chat(message="Hello", tools=[])

if __name__ == "__main__":
    print("Testing Cohere SDK patterns...")
    
    # Test synchronous patterns
    test_chat_api()
    test_generate_api()
    test_embed_api()
    test_rerank_api()
    test_compass_api()
    test_model_usage()
    test_streaming()
    test_tool_calling()
    test_non_cohere_patterns()
    
    # Test asynchronous patterns
    async def run_async_tests():
        await test_async_patterns()
        await test_compass_async()
        await test_async_streaming()
        await test_async_tool_calling()
        await test_async_functions()
    
    asyncio.run(run_async_tests())
    
    print("All Cohere SDK patterns tested!")
