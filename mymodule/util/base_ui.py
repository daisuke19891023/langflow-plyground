import os
import uuid

import streamlit as st


class ChatUI:
    def __init__(self, *, chain, title):
        self.chain = chain
        self.title: str = title
        self.prefix = self.generate_prefix()

        self.display_title()

    def generate_prefix(self):
        caller_filename = os.path.basename(os.path.splitext(__file__)[0])
        return f"{caller_filename}_{uuid.uuid4().hex}_"

    def __call__(self):
        self.react_to_user_input()

    def rewrite(self):
        self.conversation = self.initialize_state("conversation", self.chain)
        self.messages = self.initialize_state("messages", [])
        self.display_conversation()

    def initialize_state(self, key_suffix, default_value):
        key = f"{self.prefix}{key_suffix}"
        if key not in st.session_state:
            st.session_state[key] = default_value
        return st.session_state[key]

    def display_title(self):
        st.title(self.title)

    def display_conversation(self):
        for message in self.messages:
            self.display_message(message["role"], message["content"])

    def display_message(self, role, content):
        with st.chat_message(role):
            st.markdown(content)

    def react_to_user_input(self):
        prompt = st.chat_input("What is up?")
        if prompt:
            self.rewrite()
            self.add_and_display_user_message(prompt)
            response = self.get_assistant_response(prompt)
            self.add_and_display_assistant_message(response)

    def add_and_display_user_message(self, message):
        self.add_message("user", message)
        self.display_message("user", message)

    def get_assistant_response(self, prompt):
        return self.conversation.run(prompt)

    def add_and_display_assistant_message(self, message):
        self.add_message("assistant", message)
        self.display_message("assistant", message)

    def add_message(self, role, message):
        self.messages.append({"role": role, "content": message})
        # 更新後のmessagesをst.session_stateにも反映
        st.session_state[f"{self.prefix}messages"] = self.messages
