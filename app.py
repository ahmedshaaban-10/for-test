import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from main import querer , save_json_to_file,  save_query_to_file
# Create a placeholder for the main content area
main_placeholder = st.empty()
def query_view():
    st.title('score')


    selected_value = st.slider('Accuracy', min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    option = st.selectbox('Select the collection: ',('dms-sbert', 'In progress..'))
    query = st.text_input("Your Query")


    if st.button('Query'):
        save_query_to_file({"query":query, "model":option, "accuracy":selected_value })
        switch_page("score")
        
query_view()