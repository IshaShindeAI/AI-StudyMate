import streamlit as st
from groq import Groq
from pypdf import PdfReader
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI StudyMate",
    page_icon="📚"
)

st.title("📚 AI StudyMate")
st.write("Upload your study PDF and generate notes, flashcards, quizzes and revision material using AI.")


api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    api_key=api_key
)


uploaded_file = st.file_uploader(
    "Upload your PDF",
    type="pdf"
)


if uploaded_file:

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text


    st.success("PDF uploaded successfully ✅")


    if st.button("Generate Study Material"):

        with st.spinner("AI is preparing your study material..."):


            prompt = f"""
You are AI StudyMate, a smart learning assistant.

Create:

1. Simple summary notes
2. Important exam points
3. Flashcards Q&A format
4. 10 quiz questions with answers
5. Revision plan

Make it student friendly.

Study Material:

{text}
"""


            response = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]

            )


            st.subheader("📖 AI Generated Study Material")

            st.write(
                response.choices[0].message.content
            )