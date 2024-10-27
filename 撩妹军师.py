import streamlit as st
from functions import *

st.set_page_config(page_title="撩妹军师",page_icon="👧", layout="wide") 
margin_r,body,margin_l = st.columns([0.1, 3, 0.1])

with body:
    st.header("撩妹军师",divider='rainbow')
    meizi_message=""
    meizi_message=st.text_area(
        label="🤖: 妹子发给你的讯息是不是有隐藏讯息？你可以把你对象的讲话贴进以下的“妹子说什么”，让军师我来帮你分析分析！",
        placeholder ="妹子说什么？",
        height=250,
        )

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
        response=st.write_stream(gemini_chat(make_prompt(prompt, meizi_message)))
        st.session_state.messages.append(
            {"role": "assistant", "content": response})
       
