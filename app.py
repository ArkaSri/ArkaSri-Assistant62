import streamlit as st
from groq import Groq

# --- KONFIGURASI TAMPILAN ---
st.set_page_config(page_title="ArkaSri Assistant", page_icon="📚")
st.title("📚 ArkaSri AI-Assistant")
st.subheader("Rekan Profesional untuk Bapak/Ibu Guru Hebat")

# --- KONFIGURASI API ---
# Bunda tinggal masukkan API Key dari Groq di sini
api_key = st.sidebar.text_input("Masukkan Groq API Key", type="password")

if api_key:
    client = Groq(api_key=api_key)

    # --- INSTRUKSI RAHASIA (SYSTEM PROMPT) ---
    system_instruction = (
        "Kamu adalah Asisten Cerdas ArkaSri. "
        "Tugasmu membantu guru menyusun RPP/Modul dengan profesional. "
        "Panggil pengguna dengan 'Bapak/Ibu'. "
        "Dilarang keras memakai panggilan sayang atau intim. "
        "Bahasa harus sopan, santun, dan suportif. "
        "Berikan semangat di akhir jawaban. Fokus pada pendidikan Indonesia."
    )

    # --- INTERAKSI CHAT ---
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": system_instruction}]

    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("Apa yang ingin Bapak/Ibu susun hari ini?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Mengirim pesan ke mesin Groq
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
else:
    st.info("Bunda, silakan masukkan API Key dari Groq di sidebar sebelah kiri ya.")
    st.write("Dapatkan API Key gratis di: https://console.groq.com/")
