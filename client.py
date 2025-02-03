import requests

prompt = "What are the legal implications of breach of contract?"

localhost = "http://localhost:8080/embed/"
ngrok_url = "https://4cb3-2601-602-8b82-92b0-64d0-4b7b-a51a-85fb.ngrok-free.app/embed/"
response = requests.post(ngrok_url, json={"text": prompt})
print(response.json())