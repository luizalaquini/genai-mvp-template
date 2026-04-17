"""Streamlit UI for the MVP."""
import streamlit as st
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

st.set_page_config(page_title="GenAI MVP", page_icon="🤖")
st.title("🤖 GenAI MVP Template")

client = Anthropic()

user_input = st.text_input("Enter your message:")
if user_input:
    with st.spinner("Processing..."):
        response = run_chain(
            user_input=user_input,
            model_client=client,
            variables={"domain": "general assistance"}
        )
    st.write(response)