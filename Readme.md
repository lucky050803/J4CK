import ollama

response = ollama.chat(model='llama3.1', messages=[

  {
    'role': 'user',
    'content': 'Why is the sky blue?,
  },
])

print(response['message']['content'])

model a utiliser : tinyllama

from ollama import Client
client = Client(host='http://localhost:11434')
response = client.chat(model='llama3.1', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
