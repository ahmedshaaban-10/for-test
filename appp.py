import streamlit as st
import requests
import json
import os

def save_json_to_file(json_object, file_path):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the JSON object to the JSON file
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_object, json_file, ensure_ascii=False)
        print(f'JSON data has been saved to {file_path}')
    except Exception as e:
        print(f'Error saving JSON data to {file_path}: {e}')

def querer_and_save(query, collection_name, accuracy):
    # Vectorization part
    url_vectorization = "http://172.105.247.6:6000/vectorize"
    headers_vectorization = {"Content-Type": "application/json"}

    data_vectorization = {
        "element": query,
        "model": "chatgpt",
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

def chat_page():
    st.title("Chat Page")

    # Gather user input
    query = st.text_input("Enter your message:")
    collection_name = "dms-chatgpt"  # You may customize this based on your needs
    accuracy = 0.7  # You may customize this based on your needs

    # Execute the querer_and_save function only when the user provides a query
    if query:
        # Update the context with the user's input
        context = [query]

        # Use querer_and_save function
        response_retrieve = querer_and_save(query, collection_name, accuracy)

        # Display the API response
        st.write("Retrieve API Response:")
        st.json(response_retrieve.json())

def s_page():
    st.title("S Page")
    st.write("This is the S page.")

def main():
    st.set_page_config(page_title="My Streamlit App", page_icon="🌐")

    # Add a selectbox to switch between pages
    pages = ["Chat", "S"]
    selected_page = st.sidebar.selectbox("Select a page", pages)

    # Display the selected page with corresponding function
    if selected_page == "Chat":
        chat_page()
    elif selected_page == "S":
        s_page()

if __name__ == "__main__":
    main()
