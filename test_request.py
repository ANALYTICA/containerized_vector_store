import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--question", type=str, default="Can I eat mushrooms?")
args = parser.parse_args()
print(args.question)

response = requests.put(
    url='http://127.0.0.1:8000/chat/response',
    json={
        "text":args.question
    }
)

print(response.json())