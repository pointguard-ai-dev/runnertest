import boto3
import json

# Create Bedrock Runtime client
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Example request: invoke Claude v1.3 with a simple prompt
payload = {
    "prompt": "\n\nHuman: What is the capital of France?\n\nAssistant:",
    "max_tokens_to_sample": 100,
    "temperature": 0.5,
    "stop_sequences": ["\n\nHuman:"]
}

# Claude v1.3 ARN (example) – update as needed
model_id = "amazon.nova-canvas-v1:0"

try:
    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(payload)
    )

    result = json.loads(response['body'].read().decode("utf-8"))
    print("Response:")
    print(result["completion"])

except Exception as e:
    print("Error invoking model:", str(e))
