import requests
import json

# Replace with the actual URL of your Django chatbot API
url = "http://localhost:8000/api/chatbot/"

def chat_with_bot(user_input):
    # Prepare the payload
    payload = {
        "text": user_input
    }

    # Send a POST request to the chatbot API
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        print("Bot:", response_data.get("response"))
    else:
        print(f"Failed to get a response from the bot, status code: {response.status_code}")

if __name__ == "__main__":
    print("Start chatting with the bot (type 'quit' to stop)!")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        
        # Make a request to the chatbot API
        chat_with_bot(user_input)
