import requests
import json

def save_json_to_file(json_object):
    try:
        # Save the JSON object to the JSON file
        with open("../for-test/pages/data.json", 'w', encoding='utf-8') as json_file:
            json.dump(json_object, json_file, ensure_ascii=False)
        print(f'JSON data has been saved to {"data.json"}')
    except Exception as e:
        print(f'Error saving JSON data to {"data.json"}: {e}')

def save_query_to_file(json_object):
    try:
        # Save the JSON object to the JSON file
        with open("pages/query.json", 'w', encoding='utf-8') as json_file:
            json.dump(json_object, json_file, ensure_ascii=False)
        print(f'Query data has been saved to {"data.json"}')
    except Exception as e:
        print(f'Error saving JSON data to {"data.json"}: {e}')
        
def save_gptanswer_to_file(json_object):
    try:
        # Save the JSON object to the JSON file
        with open("pages/gpt_answer.json", 'w', encoding='utf-8') as json_file:
            json.dump(json_object, json_file, ensure_ascii=False)
        print(f'Query data has been saved to {"data.json"}')
    except Exception as e:
        print(f'Error saving JSON data to {"data.json"}: {e}')

#

def querer(query, collection_name, accuracy):
    server = ''
    # Vectorization part
    url_vectorization = "http://172.105.247.6:6000/vectorize"
    headers_vectorization = {"Content-Type": "application/json"}
    
    data_vectorization = {
        "element": query,
        "model" : "chatgpt",
        }
    
    response_vectorization = requests.post(url = "http://172.105.247.6:6000/vectorize", headers=headers_vectorization, json=data_vectorization)
    
    #retrieval part
    url_retrieve = "http://172.105.247.6:6000/retrieve"
    headers_retrieve = {"Content-Type": "application/json"}
    
    data_retrieve = {
        "element": response_vectorization.json()['vector'],
        "collection": collection_name,
        "accuracy": accuracy
        }
    
    response_retrieve = requests.post(url = "http://172.105.247.6:6000/retrieve", headers=headers_retrieve, json=data_retrieve)
    print("HIIIIIIIIIIIIIIIIIIIIIIIIIII", response_vectorization.json())

    return response_retrieve

def read_text_from_query(json_file_path="pages/query.json"):
    try:
        # Open the JSON file for reading
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            # Load the data from the JSON file
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f'Error: File {json_file_path} not found.')
        return None
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON in {json_file_path}: {e}')
        return None
    
def server_answering(prompt,context):
    url = "http://172.105.247.6:6000/ask"

    payload = json.dumps({
    "prompt": prompt,
    "context": context
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text