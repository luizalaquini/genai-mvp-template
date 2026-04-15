"""Streamlit UI para o MVP."""
import streamlit as st
from src.core.chains.base_chain import SimpleChain

st.set_page_config(page_title="MVP GenAI", page_icon="🤖")
st.title("🤖 MVP GenAI - Template")

if "chain" not in st.session_state:
    st.session_state.chain = SimpleChain()

user_input = st.text_input("Digite sua mensagem:")
if user_input:
    with st.spinner("Processando..."):
        response = st.session_state.chain.run(user_input)
    st.write(response)