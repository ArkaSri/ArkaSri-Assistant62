import streamlit as st
from groq import Groq
from fpdf import FPDF

# --- KONFIGURASI TAMPILAN ---
st.set_page_config(page_title="ArkaSri Assistant", page_icon="📚")
st.title("📚 ArkaSri AI-Assistant")
st.subheader("Asisten Serba Bisa untuk Bapak/Ibu Guru")

# --- KONFIGURASI API ---
api_key = st.sidebar.text_input("Masukkan Groq API Key", type="password")

if api_key:
    client = Groq(api_key=api_key)
    system_instruction = (
        "Kamu adalah Asisten Cerdas ArkaSri. Bantu Bapak/Ibu Guru menyelesaikan semua tugas "
        "dengan cerdas, profesional, dan kreatif. Berikan jawaban yang komprehensif. "
        "Panggil pengguna dengan 'Bapak/Ibu'. Bahasa sopan dan santun. Berikan semangat di akhir."
    )

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
            stream = client.chat.completions.create(messages=st.session_state.messages, model="llama3-8b-8192")
            response = stream.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # --- FITUR DOWNLOAD PDF ---
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            # Menangani karakter khusus agar tidak error
            safe_response = response.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(0, 10, txt=safe_response)
            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            st.download_button(
                label="📥 Download Jawaban sebagai PDF",
                data=pdf_output,
                file_name="Hasil_ArkaSri.pdf",
                mime="application/pdf"
            )
else:
    st.info("Bunda, silakan masukkan API Key di sidebar sebelah kiri ya.")
