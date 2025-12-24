import streamlit as st
from openai import OpenAI
import os

st.title("Fif AI 🤖")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Tulis pesan...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Kamu adalah AI asisten bernama Fif."}
        ] + st.session_state.messages
    )

    reply = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.write(reply)
