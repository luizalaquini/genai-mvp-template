"""Streamlit UI para o MVP."""
import streamlit as st
from anthropic import Anthropic
from src.core.chains.base_chain import run_chain

st.set_page_config(page_title="MVP GenAI", page_icon="🤖")
st.title("🤖 MVP GenAI - Template")

client = Anthropic()

user_input = st.text_input("Digite sua mensagem:")
if user_input:
    with st.spinner("Processando..."):
        response = run_chain(
            user_input=user_input,
            model_client=client,
            variables={"domain": "assistência geral"}
        )
    st.write(response)