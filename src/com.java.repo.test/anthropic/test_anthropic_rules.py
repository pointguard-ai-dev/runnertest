"""
Test file for Anthropic Semgrep rules - positive cases that should trigger rules
"""

import os
import asyncio
import base64

# Test 1: Import patterns (should trigger anthropic-sdk-imports)
import anthropic
from anthropic import Anthropic, AsyncAnthropic
from anthropic.client import Anthropic as AnthropicClient
import anthropic as ai

# Test 2: Client instantiation (should trigger anthropic-api-client-usage)
client = anthropic.Anthropic(api_key="sk-ant-api03-...")
async_client = anthropic.AsyncAnthropic(api_key="sk-ant-api03-...")
client2 = Anthropic(api_key="sk-ant-api03-...")
async_client2 = AsyncAnthropic(api_key="sk-ant-api03-...")

# Test 3: API key usage (should trigger anthropic-api-key-usage)
client_with_key = anthropic.Anthropic(api_key="sk-ant-api03-...")
async_client_with_key = AsyncAnthropic(api_key="sk-ant-api03-...")

# Test 4: Environment variables (should trigger anthropic-api-env-key)
api_key = os.environ.get("ANTHROPIC_API_KEY")
api_key2 = os.getenv("ANTHROPIC_API_KEY")
api_key3 = os.environ["ANTHROPIC_API_KEY"]
claude_key = os.environ.get("CLAUDE_API_KEY")

# Test 5: Base URL configuration (should trigger anthropic-api-base-url)
client_with_base = anthropic.Anthropic(base_url="https://api.anthropic.com")
custom_base = anthropic.AsyncAnthropic(base_url="https://custom.anthropic.com/v1")

# Test 6: Messages API calls (should trigger anthropic-api-messages)
def test_messages():
    client = anthropic.Anthropic(api_key="sk-ant-api03-...")
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ]
    )
    return response

# Test 7: Async messages API calls (should trigger anthropic-api-messages + anthropic-api-async-patterns)
async def test_async_messages():
    client = anthropic.AsyncAnthropic(api_key="sk-ant-api03-...")
    response = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ]
    )
    return response

# Test 8: Streaming (should trigger anthropic-api-streaming)
def test_streaming():
    client = anthropic.Anthropic(api_key="sk-ant-api03-...")
    stream = client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ]
    )
    for event in stream:
        print(event)

# Test 9: Async streaming (should trigger anthropic-api-streaming + anthropic-api-async-patterns)
async def test_async_streaming():
    client = anthropic.AsyncAnthropic(api_key="sk-ant-api03-...")
    stream = await client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ]
    )
    async for event in stream:
        print(event)

# Test 10: Context manager streaming (should trigger anthropic-api-streaming)
def test_context_streaming():
    client = anthropic.Anthropic(api_key="sk-ant-api03-...")
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ]
    ) as stream:
        for event in stream:
            print(event)

# Test 11: Async context manager streaming (should trigger anthropic-api-streaming + anthropic-api-async-patterns)
async def test_async_context_streaming():
    client = anthropic.AsyncAnthropic(api_key="sk-ant-api03-...")
    async with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ]
    ) as stream:
        async for event in stream:
            print(event)

# Test 12: Legacy completions API (should trigger anthropic-api-completions)
def test_completions():
    client = anthropic.Anthropic(api_key="sk-ant-api03-...")
    response = client.completions.create(
        model="claude-2.1",
        prompt="Human: Hello there!\n\nAssistant:",
        max_tokens_to_sample=100,
    )
    return response

# Test 13: Async completions (should trigger anthropic-api-completions + anthropic-api-async-patterns)
async def test_async_completions():
    client = anthropic.AsyncAnthropic(api_key="sk-ant-api03-...")
    response = await client.completions.create(
        model="claude-2.1",
        prompt="Human: Hello there!\n\nAssistant:",
        max_tokens_to_sample=100,
    )
    return response

# Test 14: Model usage (should trigger anthropic-api-model-usage)
def test_model_usage():
    client = anthropic.Anthropic(api_key="sk-ant-api03-...")
    
    # Specific model names
    response1 = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    response2 = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    response3 = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": "Hello"}]
    )
    
    # Variable with claude in name
    claude_model = "claude-3-sonnet-20240229"
    response4 = client.messages.create(
        model=claude_model,
        max_tokens=1000,
        messages=[{"role": "user", "content": "Hello"}]
    )

# Test 15: Tool/function calling (should trigger anthropic-api-tool-calling)
def test_tool_calling():
    client = anthropic.Anthropic(api_key="sk-ant-api03-...")
    
    tools = [
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"}
                },
                "required": ["location"]
            }
        }
    ]
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        tools=tools,
        tool_choice="auto",
        messages=[
            {"role": "user", "content": "What's the weather like in San Francisco?"}
        ]
    )
    return response

# Test 16: Async tool calling (should trigger anthropic-api-tool-calling + anthropic-api-async-patterns)
async def test_async_tool_calling():
    client = anthropic.AsyncAnthropic(api_key="sk-ant-api03-...")
    
    tools = [
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"}
                },
                "required": ["location"]
            }
        }
    ]
    
    response = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        tools=tools,
        tool_choice="auto",
        messages=[
            {"role": "user", "content": "What's the weather like in San Francisco?"}
        ]
    )
    return response

# Test 17: Vision/image processing (should trigger anthropic-api-vision)
def test_vision():
    client = anthropic.Anthropic(api_key="sk-ant-api03-...")
    
    image_data = base64.b64encode(b"fake image data").decode()
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "content": "What's in this image?"
                    }
                ]
            }
        ]
    )
    return response

# Test 18: Vision with URL (should trigger anthropic-api-vision)
def test_vision_url():
    client = anthropic.Anthropic(api_key="sk-ant-api03-...")
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": "https://example.com/image.jpg"
                        }
                    },
                    {
                        "type": "text",
                        "content": "What's in this image?"
                    }
                ]
            }
        ]
    )
    return response

# Test 19: Message roles (should trigger anthropic-api-message-roles)
def test_message_roles():
    client = anthropic.Anthropic(api_key="sk-ant-api03-...")
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
            {"role": "user", "content": "That's great to hear!"}
        ]
    )
    return response

# Test 20: System prompts (should trigger anthropic-api-system-prompts)
def test_system_prompts():
    client = anthropic.Anthropic(api_key="sk-ant-api03-...")
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        system="You are a helpful assistant that always responds in a friendly manner.",
        messages=[
            {"role": "user", "content": "Hello!"}
        ]
    )
    return response

# Test 21: Async system prompts (should trigger anthropic-api-system-prompts + anthropic-api-async-patterns)
async def test_async_system_prompts():
    client = anthropic.AsyncAnthropic(api_key="sk-ant-api03-...")
    
    response = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        system="You are a helpful assistant that always responds in a friendly manner.",
        messages=[
            {"role": "user", "content": "Hello!"}
        ]
    )
    return response

# Test 22: Configuration patterns (should trigger anthropic-api-configuration)
def test_configuration():
    client = anthropic.Anthropic(
        api_key="sk-ant-api03-...",
        timeout=30.0,
        max_retries=3
    )
    
    async_client = anthropic.AsyncAnthropic(
        api_key="sk-ant-api03-...",
        timeout=60.0,
        max_retries=5
    )
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0.7,
        messages=[
            {"role": "user", "content": "Hello!"}
        ]
    )
    return response

# Test 23: Complex async function (should trigger anthropic-api-async-patterns)
async def complex_async_function():
    client = anthropic.AsyncAnthropic(api_key="sk-ant-api03-...")
    
    # Multiple await calls
    response1 = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": "First message"}]
    )
    
    response2 = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": "Second message"}]
    )
    
    return response1, response2

if __name__ == "__main__":
    # Run sync tests
    test_messages()
    test_streaming()
    test_context_streaming()
    test_completions()
    test_model_usage()
    test_tool_calling()
    test_vision()
    test_vision_url()
    test_message_roles()
    test_system_prompts()
    test_configuration()
    
    # Run async tests
    asyncio.run(test_async_messages())
    asyncio.run(test_async_streaming())
    asyncio.run(test_async_context_streaming())
    asyncio.run(test_async_completions())
    asyncio.run(test_async_tool_calling())
    asyncio.run(test_async_system_prompts())
    asyncio.run(complex_async_function())
    
    print("All Anthropic tests completed!")
