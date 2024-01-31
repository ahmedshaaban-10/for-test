import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from main import querer, read_text_from_query, server_answering, save_gptanswer_to_file

# Create a placeholder for the main content area
main_placeholder = st.empty()

def score_view():
    st.title('View of DB Search')
    query = read_text_from_query().get("query", "")
    model = read_text_from_query().get("model", "")
    accuracy = read_text_from_query().get("accuracy", "")

    st.markdown(':red[Your] :orange[Query] :green[is:] ')
    st.markdown(f'{read_text_from_query().get("query", "")}')

    st.markdown('''
    :red[Your] :orange[Model] :green[is:] ''')
    st.markdown(f'{read_text_from_query().get("model", "")}')

    st.markdown('''
    :red[Your] :orange[Accuracy] :green[is:] ''')
    st.markdown(f'{read_text_from_query().get("accuracy", "")}')

    response = querer(query, model, accuracy)
    
    # List to store the checked checkboxes
    checked_checkboxes = []
    
    for x in response.json().get("searched_list", ""):
        # Use a checkbox and store the result in the checked_checkboxes list
        checked = st.checkbox(x)
        if checked:
            checked_checkboxes.append(x)

    if st.button('GPT-Answer'):
        # Use the checked_checkboxes list as needed
        gpt_answer = server_answering(query, checked_checkboxes)
        save_gptanswer_to_file(gpt_answer)
        switch_page("gpt")

score_view()
