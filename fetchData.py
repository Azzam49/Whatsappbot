import requests

def fetch_questions(BOT_ID):
    domain = "http://azzam49.pythonanywhere.com/"
    api = f"api/get/bot_questions_by_bot_id/{BOT_ID}"
    response = requests.get(domain + api)
    
    if response.status_code == 200:
        json_data = response.json()
        questions_dict = {entry['question']: entry['answer'] for entry in json_data['bot']['data']}
        #For each entry, it extracts the 'question' and 'answer' values and assigns them as key-value pairs in the questions_dict dictionary
        lowercase_questions_dict = {question.lower(): answer for question, answer in questions_dict.items()}
        #For each question and answer in questions_dict.items(), it converts the question to lowercase using the lower() method and assigns the lowercase question as the key in the lowercase_questions_dict dictionary
        return lowercase_questions_dict
    else:
        print("Error getting JSON data.")
        return {}