#!/usr/bin/env python3
"""
Test script to validate the improved DeepSeek Semgrep rules.
This script contains various DeepSeek API usage patterns that should be detected.
"""

import os
import openai
from openai import OpenAI, AsyncOpenAI
import asyncio

# Test 1: DeepSeek client instantiation patterns
client1 = openai.OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

client2 = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

async_client = AsyncOpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# Test 2: DeepSeek API key environment variables
api_key1 = os.environ.get("DEEPSEEK_API_KEY")
api_key2 = os.getenv("DEEPSEEK_KEY")
api_key3 = os.environ["DEEPSEEK_TOKEN"]

# Test 3: DeepSeek chat completions API calls
response1 = client1.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

response2 = client2.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "user", "content": "Solve this math problem: 2+2=?"}
    ]
)

# Test 4: DeepSeek streaming responses
def test_streaming():
    stream = client1.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Tell me a story"}],
        stream=True,
        max_tokens=1000
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

# Test 5: DeepSeek async patterns
async def test_async_chat():
    response = await async_client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Hello async world!"}],
        temperature=0.7
    )
    return response.choices[0].message.content

# Test 6: DeepSeek tool/function calling
def test_function_calling():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string"}
                    }
                }
            }
        }
    ]
    
    response = client1.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "What's the weather in New York?"}],
        tools=tools
    )
    return response

# Test 7: DeepSeek JSON output mode
def test_json_output():
    response = client1.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Generate a JSON object with name and age"}],
        response_format={"type": "json_object"}
    )
    return response

# Test 8: DeepSeek response processing
def test_response_processing():
    response = client1.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    
    content = response.choices[0].message.content
    model_used = response.model
    
    return content, model_used

# Test 9: DeepSeek high-risk usage patterns
def test_high_risk_usage(user_input):
    response = client1.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    return response

# Test 10: DeepSeek streaming response handling
def test_streaming_response():
    for chunk in client1.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": "Explain quantum computing"}],
        stream=True,
        max_tokens=2000
    ):
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="")

# Test 11: DeepSeek parameter configurations
def test_parameter_usage():
    response = client1.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Generate creative content"}],
        temperature=0.9,
        max_tokens=4000,
        top_p=0.95
    )
    return response

if __name__ == "__main__":
    print("Testing DeepSeek API patterns...")
    
    # Test synchronous chat
    try:
        response = test_response_processing()
        print("Sync response received:", response[0][:50] + "...")
    except Exception as e:
        print("Sync test failed:", e)
    
    # Test async chat
    try:
        asyncio.run(test_async_chat())
        print("Async test completed")
    except Exception as e:
        print("Async test failed:", e)
    
    print("Test script completed!")
