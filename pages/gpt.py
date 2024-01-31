import json
import streamlit as st
from main import read_text_from_query

st.json(read_text_from_query("pages/gpt_answer.json"))