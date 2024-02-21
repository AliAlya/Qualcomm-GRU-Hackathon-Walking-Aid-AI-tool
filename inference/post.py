import requests

url = 'https://v6ma9h036i.execute-api.us-east-1.amazonaws.com/default/gait'
data = {
    "id": "1",
    "value": str(0.3)
}
response = requests.post(url, json=data)

# Check the response
print(response.status_code)
print(response.text)
response = requests.post(url, json=data)