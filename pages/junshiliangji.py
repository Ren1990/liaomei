import streamlit as st
from functions import *

st.set_page_config(page_title="坐筹帷幄",page_icon="💡", layout="wide") 
margin_r,body,margin_l = st.columns([0.1, 3, 0.1])

with body:
    menu()
    st.header("坐筹帷幄",divider='rainbow')
if "messages" not in st.session_state:
    #st.session_state.table=update_knowledge()
    st.session_state.messages = []
    
# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"]=="user":
        with st.chat_message("user",avatar="🧒🏻"):
            st.markdown(message["content"])
    if message["role"]=="assistant":
        with st.chat_message("assistant",avatar="🤖"):
            st.markdown(message["content"])

if prompt := st.chat_input("军师救救我"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user","content": prompt})
    # Display user message in chat message container
    with st.chat_message("user",avatar="🧒🏻"):
        st.markdown(prompt)

    #passage=retrieve_knowledge(prompt)

    with st.chat_message("assistant",avatar="🤖"):
        response=st.write_stream(gemini_chat(make_prompt2(prompt)))
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
       
