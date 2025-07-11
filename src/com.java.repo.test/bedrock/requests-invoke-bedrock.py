import requests
import json

url = "https://bedrock-runtime.us-east-1.amazonaws.com/model/mistral.mistral-7b-instruct-v0:2/invoke"

payload = json.dumps({
  "prompt": "Write about your company appsoc",
  "max_tokens": 200,
  "temperature": 0.5,
  "top_p": 0.9,
  "top_k": 50
})
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'X-Amz-Content-Sha256': 'beaead3198f7da1e70d03ab969765e0821b24fc913697e929e726aeaebf0eba3',
  'X-Amz-Date': '20250626T071051Z',
  'Authorization': 'AWS4-HMAC-SHA256 Credential=AKIAU6GDWG2LLXWHFIMJ/20250626/us-east-1/bedrock/aws4_request, SignedHeaders=accept;content-length;content-type;host;x-amz-content-sha256;x-amz-date, Signature=31a468dfbe78d1e1a00d85d602359fb533d823bfe2cfe322c3fa5b1048ec01bd'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
