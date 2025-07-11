# Test file to validate OpenGREP Bedrock rules
import boto3
import json
from langchain_aws import ChatBedrockConverse, BedrockEmbeddings

# Bedrock client initialization patterns
bedrock_client = boto3.client('bedrock')
bedrock_runtime = boto3.client('bedrock-runtime')
bedrock_agent_client = boto3.client('bedrock-agent')
bedrock_agent_runtime_client = boto3.client('bedrock-agent-runtime')

# Session-based client creation
session = boto3.session.Session()
bedrock = session.client('bedrock-runtime')

# Model invocation patterns
response = bedrock.invoke_model(
    modelId='anthropic.claude-3-sonnet-20240229-v1:0',
    body=json.dumps(request_body)
)

# Different modelId parameter patterns
response2 = bedrock_runtime.invoke_model(
    modelId="amazon.nova-pro-v1:0",
    body=body_content
)

# Converse API usage
response = bedrock.converse(
    modelId='us.anthropic.claude-3-haiku-20240307-v1:0',
    messages=messages,
    inferenceConfig={
        'temperature': 0.7,
        'maxTokens': 1000
    }
)

# Streaming converse
response = bedrock.converse_stream(
    modelId='amazon.nova-pro-v1:0',
    messages=messages
)

# Knowledge Base operations
kb_response = bedrock_agent_runtime_client.retrieve_and_generate(
    input={'text': query},
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': kb_id,
            'modelArn': model_arn
        }
    }
)

# Retrieve API
retrieve_response = bedrock_agent_runtime_client.retrieve(
    knowledgeBaseId=kb_id,
    retrievalQuery={'text': query}
)

# Agent operations
agent_response = bedrock_agent_runtime_client.invoke_agent(
    agentId=agent_id,
    agentAliasId=agent_alias_id,
    sessionId=session_id,
    inputText=query
)

# Model management
models = bedrock.list_foundation_models()
custom_models = bedrock.list_custom_models()

# Cross-region inference
inference_profiles = bedrock.list_inference_profiles()

# Model ARNs
model_arn = f"arn:aws:bedrock:{region}::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
titan_arn = "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"

# Different model IDs
claude_model = "anthropic.claude-3-haiku-20240307-v1:0"
nova_model = "us.amazon.nova-lite-v1:0"
llama_model = "us.meta.llama3-1-70b-instruct-v1:0"
titan_model = "amazon.titan-embed-text-v2:0"

# LangChain integration
llm = ChatBedrockConverse(
    model='us.amazon.nova-pro-v1:0',
    temperature=0,
    max_tokens=None,
    client=bedrock_runtime,
)

embeddings = BedrockEmbeddings(
    client=bedrock_runtime,
    model_id="amazon.titan-embed-text-v1"
)

# Function calling configuration
tool_config = {
    "tools": [
        {
            "toolSpec": {
                "name": "get_weather",
                "description": "Get weather information",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string"}
                        }
                    }
                }
            }
        }
    ]
}

# Inference configuration
inference_config = {
    "temperature": 0.7,
    "topP": 0.9,
    "maxTokens": 500
}

# Message structure
messages = [
    {
        "role": "user",
        "content": [
            {"text": "Hello, how are you?"}
        ]
    }
]

# System message
system_prompt = [
    {"text": "You are a helpful assistant."}
]

# Error handling
try:
    response = bedrock.converse(modelId=model_id, messages=messages)
except botocore.exceptions.ClientError as error:
    if error.response['Error']['Code'] == 'AccessDeniedException':
        print("Access denied to Bedrock")

# Streaming response handling
response_stream = response.get('stream')
if response_stream:
    for event in response_stream:
        if 'contentBlockDelta' in event:
            delta = event['contentBlockDelta']['delta']
            if 'text' in delta:
                print(delta['text'], end='')

# IAM permissions
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:Retrieve",
                "bedrock:RetrieveAndGenerate"
            ],
            "Resource": [
                f"arn:aws:bedrock:{region}::foundation-model/*"
            ]
        }
    ]
}

# Service assumption
assume_role_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {
            "Service": "bedrock.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
    }]
}
