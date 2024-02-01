import streamlit as st
import requests
import json
import os
from func import save_json_to_file
from func import querer_and_save ,create_prompt,read_retrieval_result,ask_question


def chat_page():
    st.title("Chatgpt")

    # Gather user input
    query = st.text_input("Enter your message:")
    collection_name = "dms-chatgpt"  # You may customize this based on your needs

    # Create a slider for the accuracy parameter
    accuracy = st.slider("Select Accuracy", 0.0, 1.0, 0.5, step=0.01)

    # Create a select box for choosing the model
    model_options = ["chatgpt", "sbert"]
    selected_model = st.selectbox("Choose Model", model_options)

    # Button to trigger the function
    if st.button("Run Functions"):
        # Update the context with the user's input
        context = [query]

        # Use querer_and_save function
        response_retrieve = querer_and_save(query, collection_name, accuracy, model=selected_model)

        # Display the API response
        st.write("Retrieve API Response:")
        st.json(response_retrieve.json())

        # Read the content of retrieval_result.json
        retrieval_result = read_retrieval_result()

        if retrieval_result:
            # Include retrieval_result in context for ask_question
            context.append(retrieval_result)

            # Use the response to make a new request to "http://172.105.247.6:6000/ask"
            ask_response = ask_question(context, model=selected_model)

            # Print the entire Ask API Response
            st.write("Ask API Response:")
            st.json(ask_response)

            # Create and save the prompt
            merged_text = create_prompt(response_retrieve.json(), query)


def main():
    st.set_page_config(page_title="My Streamlit App", page_icon="🌐")

    # Add a selectbox to switch between pages
    pages = ["chatgpt"]
    chat_page()

if __name__ == "__main__":
    main()
