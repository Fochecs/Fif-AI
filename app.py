import streamlit as st
from openai import OpenAI
import os
import json
from pathlib import Path

# =========================
# KONFIGURASI UTAMA (EDIT DI SINI SAJA)
# =========================
AI_NAME = "Fif AI"
AI_EMOJI = "😁"
SYSTEM_PROMPT = (
    "Nama kamu adalah Fif. "
    "Kamu adalah asisten AI yang ramah, jelas, dan membantu. "
    "Jawab singkat tapi bernilai."
)

MODEL_NAME = "gpt-4.1-mini"
HISTORY_FILE = Path("chat_history.json")

# =========================
# SETUP HALAMAN
# =========================
st.set_page_config(
    page_title=AI_NAME,
    page_icon="🤖",
    layout="centered"
)

st.title(f"{AI_NAME} {AI_EMOJI}")

# =========================
# OPENAI CLIENT
# =========================
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# =========================
# LOAD / INIT CHAT HISTORY
# =========================
if "messages" not in st.session_state:
    if HISTORY_FILE.exists():
        try:
            st.session_state.messages = json.loads(HISTORY_FILE.read_text())
        except Exception:
            st.session_state.messages = []
    else:
        st.session_state.messages = []

# =========================
# TAMPILKAN CHAT SEBELUMNYA
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# =========================
# INPUT USER
# =========================
prompt = st.chat_input("Tulis pesan...")

if prompt:
    # simpan pesan user
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    # =========================
    # PANGGIL AI (PAKAI GUARD)
    # =========================
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT}
            ] + st.session_state.messages
        )

        reply = response.choices[0].message.content

    except Exception:
        reply = "⚠️ Lagi ada gangguan sebentar. Coba ulangi ya."

    # simpan jawaban AI
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    # simpan ke file (memory)
    try:
        HISTORY_FILE.write_text(
            json.dumps(st.session_state.messages, ensure_ascii=False)
        )
    except Exception:
        pass

    with st.chat_message("assistant"):
        st.write(reply)

