import requests
import json

def post_user_question(question, answer):
    # Define the API endpoint URL
    url = "http://azzam49.pythonanywhere.com/api/post/create_question_by_bot_id/12345/"

    # Create a dictionary with the payload data
    payload = {
        "question": question,
        "answer": answer
    }

    # Convert the payload to JSON
    json_payload = json.dumps(payload)

    # Set the request headers
    headers = {
        "Content-Type": "application/json"
    }

    # Send the POST request
    try:
        response = requests.post(url, data=json_payload, headers=headers)
    except:
        return 'Failed to post question'

    # Check the response status code
    if response.status_code == 200:
        # Request successful
        print("POST request successful!")
    else:
        # Request failed
        print("POST request failed.")