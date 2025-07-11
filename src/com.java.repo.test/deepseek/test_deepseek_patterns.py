#!/usr/bin/env python3
"""
Test script to validate OpenGREP rules against DeepSeek API usage patterns.
This script demonstrates various patterns that should be detected by the DeepSeek rules.
"""

import os
import asyncio
from openai import OpenAI, AsyncOpenAI

# Rule 1 & 2: Import and instantiation patterns
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key="your-deepseek-api-key"
)

async_client = AsyncOpenAI(
    base_url="https://api.deepseek.com",
    api_key="your-deepseek-api-key"
)

# Rule 7: API key usage patterns
deepseek_api_key = "sk-deepseek-12345"
client_with_key = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=deepseek_api_key
)

# Rule 8: Environment variable usage
api_key_from_env = os.environ.get("DEEPSEEK_API_KEY")
client_with_env = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=api_key_from_env
)

# Alternative environment variable patterns
deepseek_key = os.getenv("DEEPSEEK_KEY")
client_alt_env = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=deepseek_key
)

def test_deepseek_chat():
    """Rule 3 & 5: Chat completions API calls and model usage"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"}
        ],
        max_tokens=1024,
        temperature=0.7
    )
    
    # Rule 11: Response processing
    print(response.choices[0].message.content)
    return response

def test_deepseek_coder():
    """Rule 12: DeepSeek Coder model usage"""
    response = client.chat.completions.create(
        model="deepseek-coder",
        messages=[
            {"role": "user", "content": "Write a Python function to calculate fibonacci numbers"}
        ],
        max_tokens=512,
        temperature=0.1
    )
    
    print(response.choices[0].message.content)
    return response

def test_deepseek_reasoning():
    """Rule 13: DeepSeek Reasoning model usage"""
    response = client.chat.completions.create(
        model="deepseek-r1",
        messages=[
            {"role": "user", "content": "Solve this logic puzzle: If all roses are flowers and some flowers fade quickly, what can we conclude?"}
        ],
        max_tokens=1024,
        temperature=0.3
    )
    
    print(response.choices[0].message.content)
    return response

def test_streaming():
    """Rule 4: Streaming responses"""
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Tell me a story"}],
        stream=True,
        max_tokens=512
    )
    
    # Rule 4: Streaming iteration
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            # Rule 11: Response processing
            print(chunk.choices[0].delta.content, end="", flush=True)

async def test_async_deepseek():
    """Rule 10: Async patterns"""
    response = await async_client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Hello"}],
        stream=True,
    )
    
    # Rule 10: Async streaming
    async for chunk in response:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="", flush=True)

def test_tool_calling():
    """Rule 6: Tool/function calling"""
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City and country e.g. Paris, France",
                        }
                    },
                    "required": ["location"],
                    "additionalProperties": False,
                },
            },
        }
    ]
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "What's the weather like in Tokyo?"}],
        tools=tools,
        max_tokens=512
    )
    return response

def test_parameter_usage():
    """Rule 18: Parameter configuration"""
    # Test various parameter configurations
    response1 = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": "Hello"}],
        temperature=0.8,
        max_tokens=100,
        top_p=0.9
    )
    
    response2 = client.chat.completions.create(
        model="deepseek-coder-33b",
        messages=[{"role": "user", "content": "Write code"}],
        temperature=0.1,
        max_tokens=1024
    )
    
    return response1, response2

def test_model_variants():
    """Rule 5, 12, 13: Different DeepSeek model variants"""
    models_to_test = [
        "deepseek-chat",
        "deepseek-coder",
        "deepseek-coder-6.7b", 
        "deepseek-coder-33b",
        "deepseek-reasoning",
        "deepseek-r1",
        "deepseek-r1-distill",
        "deepseek-v3"
    ]
    
    results = []
    for model in models_to_test:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": f"Hello from {model}"}],
                max_tokens=50
            )
            results.append((model, response.choices[0].message.content))
        except Exception as e:
            results.append((model, f"Error: {e}"))
    
    return results

def test_high_risk_patterns():
    """Rule 16: High-risk usage patterns"""
    # Simulate user input scenarios
    user_input = "Process this user data"
    
    # This pattern should be flagged as high-risk
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )
    
    # Another risky pattern - string concatenation
    form_data = "Some sensitive form data"
    response2 = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "Process this: " + form_data}
        ]
    )
    
    return response, response2

def test_config_patterns():
    """Rule 17: Configuration patterns"""
    # JSON-like configuration that might be detected
    config = {
        "model": "deepseek-chat",
        "base_url": "https://api.deepseek.com",
        "api_key": "your-key-here",
        "temperature": 0.7,
        "max_tokens": 1024
    }
    
    # Using config in API call
    response = client.chat.completions.create(
        model=config["model"],
        messages=[{"role": "user", "content": "Hello"}],
        temperature=config["temperature"],
        max_tokens=config["max_tokens"]
    )
    
    return response

# Alternative base URL patterns that should be detected
def test_alternative_urls():
    """Rule 9: Different base URL patterns"""
    # Different ways to specify DeepSeek API
    client1 = OpenAI(base_url="https://api.deepseek.com/v1")
    client2 = OpenAI(base_url="https://api.deepseek.com/")
    
    deepseek_url = "https://api.deepseek.com"
    client3 = OpenAI(base_url=deepseek_url)
    
    return client1, client2, client3

if __name__ == "__main__":
    print("Testing DeepSeek API patterns...")
    
    # Test synchronous patterns
    print("1. Testing chat completions...")
    test_deepseek_chat()
    
    print("\n2. Testing DeepSeek Coder...")
    test_deepseek_coder()
    
    print("\n3. Testing DeepSeek Reasoning...")
    test_deepseek_reasoning()
    
    print("\n4. Testing streaming...")
    test_streaming()
    
    print("\n5. Testing tool calling...")
    test_tool_calling()
    
    print("\n6. Testing parameter usage...")
    test_parameter_usage()
    
    print("\n7. Testing model variants...")
    test_model_variants()
    
    print("\n8. Testing configuration patterns...")
    test_config_patterns()
    
    print("\n9. Testing alternative URLs...")
    test_alternative_urls()
    
    # Test asynchronous patterns
    print("\n10. Testing async patterns...")
    asyncio.run(test_async_deepseek())
    
    # Test high-risk patterns (commented out to avoid actual execution)
    # print("\n11. Testing high-risk patterns...")
    # test_high_risk_patterns()
    
    print("\n\nAll DeepSeek test patterns executed!")
    print("These patterns should be detected by the OpenGREP rules.")
