#!/usr/bin/env python3
"""
Comprehensive test file for Gemini/Google Generative AI Semgrep rules.
This file contains positive test cases for all rule types.
"""

import os
import asyncio
import PIL.Image
import google.generativeai
import google.generativeai as genai
from google import generativeai
from google.generativeai import embed_content, batch_embed_contents
from google.generativeai.types import HarmCategory, HarmBlockThreshold, GenerationConfig
from google.generativeai.protos import Tool, FunctionDeclaration, Content, Part, Blob, FileData
from google.ai.generativelanguage import GenerativeServiceClient


# 1. Configuration Examples
def test_configuration():
    """Test Gemini API configuration patterns."""
    # Basic configuration
    google.generativeai.configure(api_key="your-api-key")
    generativeai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Configuration with additional parameters
    google.generativeai.configure(
        api_key="your-api-key",
        transport="rest"
    )


# 2. Model Creation Examples
def test_model_creation():
    """Test Gemini model creation patterns."""
    # Basic model creation
    model = google.generativeai.GenerativeModel("gemini-pro")
    model = generativeai.GenerativeModel("gemini-1.5-pro")
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Model with configuration
    model = google.generativeai.GenerativeModel(
        "gemini-pro",
        generation_config=GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=1000
        )
    )
    
    # Model with safety settings
    model = generativeai.GenerativeModel(
        "gemini-1.5-pro",
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
    )
    
    # Model with tools
    model = google.generativeai.GenerativeModel(
        "gemini-pro",
        tools=[Tool(function_declarations=[
            FunctionDeclaration(
                name="get_weather",
                description="Get weather information",
                parameters={"type": "object", "properties": {"location": {"type": "string"}}}
            )
        ])]
    )


# 3. Generate Content Examples
def test_generate_content():
    """Test Gemini generate content patterns."""
    model = google.generativeai.GenerativeModel("gemini-pro")
    
    # Basic generation
    response = model.generate_content("Hello, world!")
    response = model.generate_content("What is the capital of France?")
    
    # Generation with config
    response = model.generate_content(
        "Write a poem",
        generation_config=GenerationConfig(temperature=0.9)
    )
    
    # Generation with safety settings
    response = model.generate_content(
        "Tell me a story",
        safety_settings={HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE}
    )
    
    # Generation with tools
    response = model.generate_content(
        "What's the weather like?",
        tools=[Tool(function_declarations=[FunctionDeclaration(name="get_weather")])]
    )


# 4. Chat Examples
def test_chat():
    """Test Gemini chat patterns."""
    model = generativeai.GenerativeModel("gemini-pro")
    
    # Start chat
    chat = model.start_chat()
    chat = model.start_chat(history=[])
    
    # Send messages
    response = chat.send_message("Hello!")
    response = chat.send_message("How are you?")
    
    # Send message with tools
    response = chat.send_message(
        "What's the weather?",
        tools=[Tool(function_declarations=[FunctionDeclaration(name="get_weather")])]
    )
    
    # Send message with safety settings
    response = chat.send_message(
        "Tell me about history",
        safety_settings={HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE}
    )


# 5. Streaming Examples
def test_streaming():
    """Test Gemini streaming patterns."""
    model = google.generativeai.GenerativeModel("gemini-1.5-flash")
    
    # Streaming generation
    response = model.generate_content("Write a long story", stream=True)
    for chunk in response:
        print(chunk.text)
    
    # Streaming chat
    chat = model.start_chat()
    response = chat.send_message("Tell me a long story", stream=True)
    for chunk in response:
        print(chunk.text)


# 6. Vision/Multimodal Examples
def test_vision():
    """Test Gemini vision/multimodal patterns."""
    model = generativeai.GenerativeModel("gemini-pro-vision")
    
    # Upload and use image
    image_file = google.generativeai.upload_file("image.jpg")
    image = PIL.Image.open("local_image.jpg")
    
    # Generate content with image
    response = model.generate_content(["Describe this image", image])
    response = model.generate_content(["What do you see?", image_file])
    
    # Chat with image
    chat = model.start_chat()
    response = chat.send_message(["Analyze this image", image])


# 7. Embeddings Examples
def test_embeddings():
    """Test Gemini embeddings patterns."""
    # Single embedding
    result = google.generativeai.embed_content(
        content="Hello world",
        model="text-embedding-004"
    )
    
    result = generativeai.embed_content(
        content="Some text to embed",
        model="embedding-001"
    )
    
    # Batch embeddings
    result = google.generativeai.batch_embed_contents(
        requests=[
            {"content": "First text"},
            {"content": "Second text"}
        ],
        model="text-embedding-004"
    )
    
    result = generativeai.batch_embed_contents(
        requests=[
            {"content": "Text 1"},
            {"content": "Text 2"}
        ]
    )


# 8. Async Examples
async def test_async():
    """Test Gemini async patterns."""
    model = google.generativeai.GenerativeModel("gemini-pro")
    
    # Async generation
    response = await model.generate_content_async("Hello, async world!")
    
    # Async chat
    chat = model.start_chat()
    response = await chat.send_message_async("Hello async!")


# 9. File Management Examples
def test_file_management():
    """Test Gemini file management patterns."""
    # Upload file
    file = google.generativeai.upload_file("document.pdf")
    file = generativeai.upload_file("image.jpg", mime_type="image/jpeg")
    
    # Get file
    file = google.generativeai.get_file("file_id")
    file = generativeai.get_file("file_id")
    
    # List files
    files = google.generativeai.list_files()
    for file in generativeai.list_files():
        print(file.name)
    
    # Delete file
    google.generativeai.delete_file("file_id")
    generativeai.delete_file("file_id")


# 10. Model Listing Examples
def test_model_listing():
    """Test Gemini model listing patterns."""
    # List models
    models = google.generativeai.list_models()
    for model in generativeai.list_models():
        print(model.name)
    
    # Get specific model
    model = google.generativeai.get_model("gemini-pro")
    model = generativeai.get_model("gemini-1.5-pro")


# 11. Environment Variable Examples
def test_env_vars():
    """Test environment variable usage."""
    # Google API key
    api_key = os.environ.get("GOOGLE_API_KEY")
    api_key = os.getenv("GOOGLE_API_KEY")
    api_key = os.environ["GOOGLE_API_KEY"]
    
    # Gemini API key
    api_key = os.environ.get("GEMINI_API_KEY")
    api_key = os.getenv("GEMINI_API_KEY")
    api_key = os.environ["GEMINI_API_KEY"]
    
    # Google Generative AI API key
    api_key = os.environ.get("GOOGLE_GENERATIVE_AI_API_KEY")
    api_key = os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    api_key = os.environ["GOOGLE_GENERATIVE_AI_API_KEY"]


# 12. Content Types Examples
def test_content_types():
    """Test Gemini content types patterns."""
    # Content creation
    content = google.generativeai.protos.Content(
        parts=[Part(text="Hello world")]
    )
    
    content = generativeai.protos.Content(
        parts=[Part(text="Hello")]
    )
    
    # Blob creation
    blob = google.generativeai.protos.Blob(
        mime_type="image/jpeg",
        data=b"image_data"
    )
    
    blob = generativeai.protos.Blob(
        mime_type="text/plain",
        data=b"text_data"
    )
    
    # FileData creation
    file_data = google.generativeai.protos.FileData(
        mime_type="application/pdf",
        file_uri="gs://bucket/file.pdf"
    )
    
    file_data = generativeai.protos.FileData(
        mime_type="image/png",
        file_uri="https://example.com/image.png"
    )


# 13. Function Calling Examples
def test_function_calling():
    """Test Gemini function calling patterns."""
    # Function declaration
    function = FunctionDeclaration(
        name="calculate_sum",
        description="Calculate the sum of two numbers",
        parameters={
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            }
        }
    )
    
    # Tool with function
    tool = Tool(function_declarations=[function])
    
    # Model with tools
    model = google.generativeai.GenerativeModel(
        "gemini-pro",
        tools=[tool]
    )
    
    # Generate with tools
    response = model.generate_content(
        "Calculate 5 + 3",
        tools=[tool]
    )


# 14. Safety Settings Examples
def test_safety_settings():
    """Test Gemini safety settings patterns."""
    # Safety settings
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }
    
    # Model with safety settings
    model = generativeai.GenerativeModel(
        "gemini-pro",
        safety_settings=safety_settings
    )
    
    # Generate with safety settings
    response = model.generate_content(
        "Tell me a story",
        safety_settings=safety_settings
    )


# 15. Generation Config Examples
def test_generation_config():
    """Test Gemini generation config patterns."""
    # Generation config
    config = GenerationConfig(
        temperature=0.8,
        top_p=0.95,
        top_k=40,
        max_output_tokens=2000,
        candidate_count=1
    )
    
    # Model with generation config
    model = google.generativeai.GenerativeModel(
        "gemini-1.5-pro",
        generation_config=config
    )
    
    # Generate with config
    response = model.generate_content(
        "Write a creative story",
        generation_config=config
    )


# 16. Model Usage Examples
def test_model_usage():
    """Test specific Gemini model usage patterns."""
    # Different model versions
    model_pro = generativeai.GenerativeModel(model="gemini-pro")
    model_vision = generativeai.GenerativeModel(model="gemini-pro-vision")
    model_15_pro = generativeai.GenerativeModel(model="gemini-1.5-pro")
    model_15_flash = generativeai.GenerativeModel(model="gemini-1.5-flash")
    model_10_pro = generativeai.GenerativeModel(model="gemini-1.0-pro")
    
    # Embedding models
    embedding_result = embed_content(
        content="Test text",
        model="text-embedding-004"
    )
    
    embedding_result = embed_content(
        content="Another test",
        model="embedding-001"
    )


# 17. Advanced Usage Examples
def test_advanced_usage():
    """Test advanced Gemini usage patterns."""
    # Complex multimodal generation
    model = google.generativeai.GenerativeModel("gemini-1.5-pro")
    
    # Upload multiple files
    pdf_file = google.generativeai.upload_file("document.pdf")
    image_file = generativeai.upload_file("chart.png")
    
    # Generate with multiple inputs
    response = model.generate_content([
        "Analyze this document and image",
        pdf_file,
        image_file
    ])
    
    # Complex chat with history
    chat = model.start_chat(history=[
        {"role": "user", "parts": ["Hello"]},
        {"role": "model", "parts": ["Hi there! How can I help you?"]}
    ])
    
    response = chat.send_message("Continue our conversation")


# 18. Error Handling Examples
def test_error_handling():
    """Test Gemini error handling patterns."""
    try:
        model = google.generativeai.GenerativeModel("gemini-pro")
        response = model.generate_content("Test query")
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")
    
    try:
        result = generativeai.embed_content("Test text")
        print(result.embedding)
    except Exception as e:
        print(f"Embedding error: {e}")


if __name__ == "__main__":
    # Run all tests
    test_configuration()
    test_model_creation()
    test_generate_content()
    test_chat()
    test_streaming()
    test_vision()
    test_embeddings()
    test_file_management()
    test_model_listing()
    test_env_vars()
    test_content_types()
    test_function_calling()
    test_safety_settings()
    test_generation_config()
    test_model_usage()
    test_advanced_usage()
    test_error_handling()
    
    # Run async tests
    asyncio.run(test_async())
    
    print("All Gemini test patterns executed!")
