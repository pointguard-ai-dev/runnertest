#!/usr/bin/env python3
"""
Test file to validate Cohere LLM Semgrep rules coverage.
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
import cohere as co

# Rule 2: Cohere API Client instantiation
client = cohere.Client(api_key="your-api-key")
client_v2 = cohere.ClientV2(api_key="your-api-key")
async_client = cohere.AsyncClient(api_key="your-api-key")
async_client_v2 = cohere.AsyncClientV2(api_key="your-api-key")

# Alternative client instantiation patterns
client_alt = Client(api_key="your-api-key")
client_v2_alt = ClientV2(api_key="your-api-key")
async_client_alt = AsyncClient(api_key="your-api-key")
async_client_v2_alt = AsyncClientV2(api_key="your-api-key")

# Rule 13: API key usage patterns
client_with_key = cohere.Client(api_key="co-123456789abcdef")
client_v2_with_key = cohere.ClientV2(api_key="co-123456789abcdef")

# Rule 14: Environment variable usage
api_key_env = os.environ.get("COHERE_API_KEY")
api_key_env_alt = os.getenv("COHERE_API_KEY")
api_key_env_direct = os.environ["COHERE_API_KEY"]
api_key_co = os.environ.get("CO_API_KEY")

# Rule 15: Base URL configurations
client_with_url = cohere.Client(
    api_key="your-api-key",
    base_url="https://api.cohere.ai"
)
client_v2_with_url = cohere.ClientV2(
    api_key="your-api-key", 
    base_url="https://api.cohere.com"
)

# Rule 25: Configuration patterns
client_configured = cohere.Client(
    api_key="your-api-key",
    timeout=30,
    max_retries=3
)

def test_chat_api():
    """Rule 3: Chat API calls"""
    # Basic chat
    response = client.chat(
        model="command-r",
        message="Hello, how are you?"
    )
    
    # Chat with configuration
    response = client.chat(
        model="command-r-plus",
        message="Tell me about AI",
        temperature=0.7,
        max_tokens=100,
        p=0.9,
        k=5
    )
    
    # Rule 11: Streaming responses
    stream_response = client.chat(
        model="command-r",
        message="Tell me a story",
        stream=True
    )
    
    for event in client.chat(model="command-r", message="Hello", stream=True):
        print(event)
    
    # Rule 12: Tool/function calling
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
    
    response = client.chat(
        model="command-r",
        message="What's the weather like?",
        tools=tools
    )
    
    # Tool results
    response = client.chat(
        model="command-r",
        message="What's the weather like?",
        tools=tools,
        tool_results=[{"call": {"name": "get_weather"}, "outputs": [{"weather": "sunny"}]}]
    )
    
    # Force single step
    response = client.chat(
        model="command-r",
        message="What's the weather like?",
        force_single_step=True
    )
    
    # Rule 17: RAG patterns
    documents = [
        {"text": "The weather is sunny today"},
        {"text": "Tomorrow will be rainy"}
    ]
    
    response = client.chat(
        model="command-r",
        message="What's the weather forecast?",
        documents=documents
    )
    
    # Chat with connectors
    response = client.chat(
        model="command-r",
        message="Search for recent news",
        connectors=[{"id": "web-search"}]
    )
    
    # Chat with citation quality
    response = client.chat(
        model="command-r",
        message="Tell me about climate change",
        documents=documents,
        citation_quality="accurate"
    )
    
    # Rule 27: Chat history patterns
    chat_history = [
        {"role": "USER", "message": "Hello"},
        {"role": "CHATBOT", "message": "Hi there!"},
        {"role": "USER", "message": "How are you?"}
    ]
    
    response = client.chat(
        model="command-r",
        message="What did we talk about?",
        chat_history=chat_history
    )
    
    # Chat with conversation ID
    response = client.chat(
        model="command-r",
        message="Continue our conversation",
        conversation_id="conv-123456"
    )

def test_generate_api():
    """Rule 4: Generate API calls"""
    # Basic generation
    response = client.generate(
        model="command-r",
        prompt="Once upon a time"
    )
    
    # Generate with configuration
    response = client.generate(
        model="command-r-plus",
        prompt="Write a story about AI",
        temperature=0.8,
        max_tokens=200,
        k=10,
        p=0.95
    )
    
    # Streaming generation
    response = client.generate(
        model="command-r",
        prompt="Tell me a joke",
        stream=True
    )

def test_embed_api():
    """Rule 5: Embed API calls"""
    # Basic embedding
    response = client.embed(
        model="embed-english-v3.0",
        texts=["Hello world", "How are you?"]
    )
    
    # Embedding with options
    response = client.embed(
        model="embed-multilingual-v3.0",
        texts=["Hello", "Hola", "Bonjour"],
        input_type="search_document"
    )

def test_rerank_api():
    """Rule 6: Rerank API calls"""
    documents = [
        {"text": "Carson City is the capital city of the American state of Nevada."},
        {"text": "The Commonwealth of the Northern Mariana Islands is a group of islands in the Pacific Ocean."},
        {"text": "Washington, D.C. is the capital of the United States."}
    ]
    
    response = client.rerank(
        model="rerank-english-v3.0",
        query="What is the capital of the United States?",
        documents=documents
    )
    
    # Rerank with top_n
    response = client.rerank(
        model="rerank-multilingual-v3.0",
        query="US capital",
        documents=documents,
        top_n=2
    )

def test_classify_api():
    """Rule 7: Classify API calls"""
    examples = [
        {"text": "I love this product", "label": "positive"},
        {"text": "This is terrible", "label": "negative"},
        {"text": "It's okay", "label": "neutral"}
    ]
    
    response = client.classify(
        model="command-r",
        inputs=["This is amazing!", "I hate this"],
        examples=examples
    )

def test_summarize_api():
    """Rule 8: Summarize API calls"""
    text = "This is a long text that needs to be summarized..."
    
    response = client.summarize(
        model="command-r",
        text=text,
        length="medium"
    )
    
    # Summarize with format
    response = client.summarize(
        model="command-r-plus",
        text=text,
        format="bullets",
        extractiveness="low"
    )

def test_detect_language_api():
    """Rule 9: Detect Language API calls"""
    response = client.detect_language(
        texts=["Hello world", "Bonjour le monde", "Hola mundo"]
    )

def test_model_usage():
    """Rule 10: Model usage patterns"""
    # Command models
    client.chat(model="command-r")
    client.chat(model="command-r-plus")
    client.chat(model="command-r-08-2024")
    client.chat(model="command-r-plus-08-2024")
    client.chat(model="command-nightly")
    client.chat(model="command-light")
    client.chat(model="command-light-nightly")
    
    # Embed models
    client.embed(model="embed-english-v3.0")
    client.embed(model="embed-multilingual-v3.0")
    client.embed(model="embed-english-light-v3.0")
    client.embed(model="embed-multilingual-light-v3.0")
    
    # Rerank models
    client.rerank(model="rerank-english-v3.0")
    client.rerank(model="rerank-multilingual-v3.0")
    client.rerank(model="rerank-english-v2.0")
    client.rerank(model="rerank-multilingual-v2.0")

async def test_async_patterns():
    """Rule 16: Async patterns"""
    # Async chat
    response = await async_client.chat(
        model="command-r",
        message="Hello async world"
    )
    
    # Async generate
    response = await async_client.generate(
        model="command-r",
        prompt="Async generation test"
    )
    
    # Async embed
    response = await async_client.embed(
        model="embed-english-v3.0",
        texts=["async embedding test"]
    )
    
    # Async rerank
    response = await async_client.rerank(
        model="rerank-english-v3.0",
        query="async query",
        documents=[{"text": "async document"}]
    )
    
    # Async classify
    response = await async_client.classify(
        model="command-r",
        inputs=["async classification test"]
    )
    
    # Async summarize
    response = await async_client.summarize(
        model="command-r",
        text="async summarization test text"
    )
    
    # Async detect language
    response = await async_client.detect_language(
        texts=["async language detection test"]
    )
    
    # Async streaming
    async for event in async_client.chat(model="command-r", message="Hello", stream=True):
        print(event)

async def test_async_function():
    """Async function pattern"""
    result = await async_client.chat(
        model="command-r",
        message="Hello from async function"
    )
    return result

def test_fine_tuning():
    """Rule 18: Fine-tuning patterns"""
    # List fine-tuned models
    models = client.finetuning.list_finetuned_models()
    
    # Create fine-tuned model
    finetune_job = client.finetuning.create_finetuned_model(
        name="my-custom-model",
        settings={
            "base_model": "command-r",
            "dataset_id": "dataset-123"
        }
    )
    
    # Get fine-tuned model
    model = client.finetuning.get_finetuned_model("ft-123456")
    
    # Update fine-tuned model
    updated_model = client.finetuning.update_finetuned_model(
        "ft-123456",
        name="updated-model-name"
    )
    
    # Delete fine-tuned model
    client.finetuning.delete_finetuned_model("ft-123456")

def test_connectors():
    """Rule 19: Connectors usage"""
    # List connectors
    connectors = client.connectors.list()
    
    # Create connector
    connector = client.connectors.create(
        name="my-connector",
        url="https://api.example.com"
    )
    
    # Get connector
    connector = client.connectors.get("conn-123456")
    
    # Update connector
    updated_connector = client.connectors.update(
        "conn-123456",
        name="updated-connector"
    )
    
    # Delete connector
    client.connectors.delete("conn-123456")

def test_high_risk_patterns():
    """Rule 20: High-risk usage patterns"""
    user_input = "sensitive user data"
    form_data = {"field": "value"}
    request_params = {"param": "value"}
    
    # High-risk chat
    response = client.chat(
        model="command-r",
        message=user_input  # Direct user input
    )
    
    # High-risk generate
    response = client.generate(
        model="command-r",
        prompt=user_input  # Direct user input
    )
    
    # High-risk embed
    response = client.embed(
        model="embed-english-v3.0",
        texts=[user_input]  # Direct user input
    )

def test_batch_processing():
    """Rule 24: Batch processing patterns"""
    # Batch embedding
    text_list = ["text1", "text2", "text3"]
    batch_texts = ["batch1", "batch2", "batch3"]
    
    response = client.embed(
        model="embed-english-v3.0",
        texts=text_list
    )
    
    # Batch classification
    input_list = ["input1", "input2", "input3"]
    batch_inputs = ["batch1", "batch2", "batch3"]
    
    response = client.classify(
        model="command-r",
        inputs=input_list
    )
    
    # Batch reranking
    document_list = [
        {"text": "doc1"},
        {"text": "doc2"},
        {"text": "doc3"}
    ]
    batch_documents = [
        {"text": "batch1"},
        {"text": "batch2"}
    ]
    
    response = client.rerank(
        model="rerank-english-v3.0",
        query="test query",
        documents=document_list
    )

def test_error_handling():
    """Rule 21: Error handling patterns"""
    try:
        response = client.chat(
            model="command-r",
            message="This might fail"
        )
    except cohere.CohereError as e:
        print(f"Cohere error: {e}")
    
    try:
        response = client.generate(
            model="command-r",
            prompt="This might also fail"
        )
    except cohere.CohereError as e:
        print(f"Cohere error: {e}")
    
    try:
        response = client.embed(
            model="embed-english-v3.0",
            texts=["This embedding might fail"]
        )
    except cohere.CohereError as e:
        print(f"Cohere error: {e}")
    
    # Specific error types
    try:
        response = client.chat(model="invalid-model", message="test")
    except cohere.CohereAPIError as e:
        print(f"API error: {e}")
    
    try:
        response = client.chat(model="command-r", message="test")
    except cohere.CohereConnectionError as e:
        print(f"Connection error: {e}")

def test_models_api():
    """Rule 25: Models API calls"""
    # List models
    models = client.models.list()
    
    # Get specific model
    model = client.models.get("command-r")
    
    # Check API key
    key_status = client.check_api_key()

def test_tokenization():
    """Rule 26: Tokenization patterns"""
    # Tokenize text
    tokens = client.tokenize(
        text="Hello world, this is a test",
        model="command-r"
    )
    
    # Detokenize tokens
    text = client.detokenize(
        tokens=[1, 2, 3, 4, 5],
        model="command-r"
    )

async def test_async_models_api():
    """Async models API calls"""
    # Async list models
    models = await async_client.models.list()
    
    # Async get model
    model = await async_client.models.get("command-r")
    
    # Async check API key
    key_status = await async_client.check_api_key()

async def test_async_tokenization():
    """Async tokenization patterns"""
    # Async tokenize
    tokens = await async_client.tokenize(
        text="Async tokenization test",
        model="command-r"
    )
    
    # Async detokenize
    text = await async_client.detokenize(
        tokens=[1, 2, 3, 4, 5],
        model="command-r"
    )

async def test_async_fine_tuning():
    """Async fine-tuning patterns"""
    # Async list fine-tuned models
    models = await async_client.finetuning.list_finetuned_models()
    
    # Async create fine-tuned model
    finetune_job = await async_client.finetuning.create_finetuned_model(
        name="async-custom-model",
        settings={
            "base_model": "command-r",
            "dataset_id": "dataset-123"
        }
    )
    
    # Async get fine-tuned model
    model = await async_client.finetuning.get_finetuned_model("ft-123456")
    
    # Async update fine-tuned model
    updated_model = await async_client.finetuning.update_finetuned_model(
        "ft-123456",
        name="async-updated-model"
    )
    
    # Async delete fine-tuned model
    await async_client.finetuning.delete_finetuned_model("ft-123456")

async def test_async_connectors():
    """Async connectors usage"""
    # Async list connectors
    connectors = await async_client.connectors.list()
    
    # Async create connector
    connector = await async_client.connectors.create(
        name="async-connector",
        url="https://api.example.com"
    )
    
    # Async get connector
    connector = await async_client.connectors.get("conn-123456")
    
    # Async update connector
    updated_connector = await async_client.connectors.update(
        "conn-123456",
        name="async-updated-connector"
    )
    
    # Async delete connector
    await async_client.connectors.delete("conn-123456")

if __name__ == "__main__":
    print("Testing Cohere SDK patterns...")
    
    # Test synchronous patterns
    test_chat_api()
    test_generate_api()
    test_embed_api()
    test_rerank_api()
    test_classify_api()
    test_summarize_api()
    test_detect_language_api()
    test_model_usage()
    test_fine_tuning()
    test_connectors()
    test_high_risk_patterns()
    test_batch_processing()
    test_error_handling()
    test_models_api()
    test_tokenization()
    
    # Test asynchronous patterns
    asyncio.run(test_async_patterns())
    asyncio.run(test_async_function())
    asyncio.run(test_async_models_api())
    asyncio.run(test_async_tokenization())
    asyncio.run(test_async_fine_tuning())
    asyncio.run(test_async_connectors())
    
    print("All Cohere SDK patterns tested!")
