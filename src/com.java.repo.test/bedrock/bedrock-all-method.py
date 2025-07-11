import boto3
import json
import time

# Initialize the Bedrock Runtime client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# Sample model and input payload
model_id = 'amazon.titan-text-express-v1'
content_type = 'application/json'
accept = 'application/json'
payload = {
    "inputText": "Explain AI in simple terms."
}

# 1. invoke_model
def demo_invoke_model():
    print("=== invoke_model ===")
    response = bedrock.invoke_model(
        modelId=model_id,
        body=json.dumps(payload),
        contentType=content_type,
        accept=accept
    )
    print(response['body'].read().decode())

# 2. invoke_model_with_response_stream
def demo_invoke_model_with_response_stream():
    print("=== invoke_model_with_response_stream ===")
    response = bedrock.invoke_model_with_response_stream(
        modelId=model_id,
        body=json.dumps(payload),
        contentType=content_type,
        accept=accept
    )
    for event in response['body']:
        print(event['chunk']['bytes'].decode())

# 3. start_async_invoke
def demo_start_async_invoke():
    print("=== start_async_invoke ===")
    response = bedrock.start_async_invoke(
        modelId=model_id,
        body=json.dumps(payload),
        contentType=content_type,
        accept=accept,
        outputLocation='s3://your-output-bucket/async-results/',
        inferenceConfig={}
    )
    print(response)
    return response['invocationId']

# 4. get_async_invoke
def demo_get_async_invoke(invocation_id):
    print("=== get_async_invoke ===")
    response = bedrock.get_async_invoke(
        invocationId=invocation_id
    )
    print(response)

# 5. list_async_invokes
def demo_list_async_invokes():
    print("=== list_async_invokes ===")
    response = bedrock.list_async_invokes()
    print(response)

# 6. converse
def demo_converse():
    print("=== converse ===")
    try:
        response = bedrock.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": "Tell me a joke."}],
        )
        print(response)
    except Exception as e:
        print("Converse not supported:", e)

# 7. converse_stream
def demo_converse_stream():
    print("=== converse_stream ===")
    try:
        response = bedrock.converse_stream(
            modelId=model_id,
            messages=[{"role": "user", "content": "Give me a quote."}],
        )
        for event in response['body']:
            print(event['chunk']['bytes'].decode())
    except Exception as e:
        print("Converse stream not supported:", e)

# 8. apply_guardrail
def demo_apply_guardrail():
    print("=== apply_guardrail ===")
    try:
        response = bedrock.apply_guardrail(
            guardrailIdentifier="your-guardrail-id",
            guardrailVersion="1",
            input=json.dumps(payload)
        )
        print(response)
    except Exception as e:
        print("Guardrail error (requires setup):", e)

# 9. can_paginate
def demo_can_paginate():
    print("=== can_paginate ===")
    print("Can paginate list_async_invokes:", bedrock.can_paginate('list_async_invokes'))

# 10. get_paginator
def demo_get_paginator():
    print("=== get_paginator ===")
    try:
        paginator = bedrock.get_paginator('list_async_invokes')
        for page in paginator.paginate():
            print(page)
    except Exception as e:
        print("Paginator error:", e)

# 11. get_waiter (no waiters defined for Bedrock at this time)
def demo_get_waiter():
    print("=== get_waiter ===")
    try:
        waiter = bedrock.get_waiter('model_ready')  # Not supported yet
        waiter.wait(modelId=model_id)
    except Exception as e:
        print("No waiter available:", e)

# 12. close (for explicitly closing boto3 client)
def demo_close():
    print("=== close ===")
    bedrock.close()

# Run all demos
if __name__ == "__main__":
    demo_invoke_model()
    demo_invoke_model_with_response_stream()
    invocation_id = demo_start_async_invoke()
    time.sleep(5)  # wait for async job to start
    demo_get_async_invoke(invocation_id)
    demo_list_async_invokes()
    demo_converse()
    demo_converse_stream()
    demo_apply_guardrail()
    demo_can_paginate()
    demo_get_paginator()
    demo_get_waiter()
    demo_close()
