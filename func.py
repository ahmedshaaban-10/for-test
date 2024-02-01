import streamlit as st
import requests
import json
import os

# func.py


def save_json_to_file(json_object, file_path):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the JSON object to the JSON file with proper encoding for Arabic characters
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_object, json_file, ensure_ascii=False, indent=2)
        print(f'JSON data has been saved to {file_path}')
    except Exception as e:
        print(f'Error saving JSON data to {file_path}: {e}')

def querer_and_save(query, collection_name, accuracy, model):
    # Vectorization part
    url_vectorization = "http://172.105.247.6:6000/vectorize"
    headers_vectorization = {"Content-Type": "application/json"}

    data_vectorization = {
        "element": query,
        "model": model,
    }

    response_vectorization = requests.post(url=url_vectorization, headers=headers_vectorization,
                                           json=data_vectorization)

    # Retrieval part
    url_retrieve = "http://172.105.247.6:6000/retrieve"
    headers_retrieve = {"Content-Type": "application/json"}

    data_retrieve = {
        "element": response_vectorization.json().get('vector', []),
        "collection": collection_name,
        "accuracy": accuracy
    }

    response_retrieve = requests.post(url=url_retrieve, headers=headers_retrieve, json=data_retrieve)

    # Save results to JSON files in the same path as the script
    script_path = os.path.dirname(__file__)
    save_json_to_file(response_vectorization.json(), os.path.join(script_path, "vectorization_result.json"))
    save_json_to_file(response_retrieve.json(), os.path.join(script_path, "retrieval_result.json"))

    return response_retrieve

def read_retrieval_result():
    script_path = os.path.dirname(__file__)
    retrieval_result_path = os.path.join(script_path, "retrieval_result.json")

    if os.path.exists(retrieval_result_path):
        with open(retrieval_result_path, 'r', encoding='utf-8') as json_file:
            retrieval_result = json.load(json_file)
        return retrieval_result
    else:
        return None


def ask_question(context, model="chatgpt"):
    # Convert None values to an empty string in the context
    context = ["" if element is None else element for element in context]

    url = "http://172.105.247.6:6000/ask"
    # Retrieve the prompt from the context
    prompt = context[0] if context else ""

    # Read the content of prompt.json
    script_path = os.path.dirname(__file__)
    prompt_file_path = os.path.join(script_path, "prompt.json")

    if os.path.exists(prompt_file_path):
        with open(prompt_file_path, 'r', encoding='utf-8') as json_file:
            prompt_content = json.load(json_file)

        # Use the prompt_content for the prompt
        prompt += f" {prompt_content['prompt']} {prompt_content['user_query']}"
    else:
        print(f"Prompt file 'prompt.json' not found.")
        return {"error": "Prompt file not found."}

    # Print the prompt before making the API call
    print("Prompt Sent to Chat:", prompt)

    payload = {
        "prompt": prompt,
        "context": {"src": context},  # Assuming the API expects "src" property
        "temperature": 0.5
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)

        # Extract the result from the response
        result = response.json().get('result', '')

        # Display the result in a larger text area in Streamlit
        st.write("Ask API Result:")
        st.text_area("", result, height=200)

        return result
    except requests.exceptions.RequestException as e:
        print(f"Error making request to 'http://172.105.247.6:6000/ask': {e}")
        return {"error": "Failed to retrieve a response."}


def create_prompt(response_retrieve, query):
    # Merge text from different sources into a single JSON object
    merged_text = {
        "response_retrieve": response_retrieve,
        "prompt": "اجب علي السؤال التالي وفقا للمعلومات السابقه فقط: ",
        "user_query": query
    }

    # Save merged text to prompt.json
    script_path = os.path.dirname(__file__)
    save_json_to_file(merged_text, os.path.join(script_path, "prompt.json"))
    print("Merged Text has been saved to prompt.json")

    return merged_text
