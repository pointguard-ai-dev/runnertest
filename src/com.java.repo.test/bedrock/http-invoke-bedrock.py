import http.client
import json

conn = http.client.HTTPSConnection("bedrock-runtime.us-east-1.amazonaws.com")
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
  'X-Amz-Content-Sha256': '••••••',
  'X-Amz-Date': '••••••',
  'Authorization': '••••••'
}
conn.request("POST", "/model/mistral.mistral-7b-instruct-v0:2/invoke", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))