#!/usr/bin/env python
"""Python file to serve as the frontend"""
import os
import datetime
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")

# From here down is all the StreamLit UI.

st.header("LangChain Demo")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []



with st.form(key="form", clear_on_submit=True):
    user_input: str = st.text_area("You: ", "", key="input_text", placeholder="please type here")
    submit: bool = st.form_submit_button("Submit")