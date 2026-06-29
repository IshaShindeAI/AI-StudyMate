import streamlit as st
from groq import Groq
from pypdf import PdfReader


st.set_page_config(
    page_title="AI StudyMate",
    page_icon="📚"
)


st.title("📚 AI StudyMate")
st.write(
    "Upload your study PDF and generate notes, flashcards, quizzes and revision material using AI."
)


# Groq API from Streamlit secrets
client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
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


    # Limit PDF size for Groq free tier
    text = text[:12000]


    st.success("PDF uploaded successfully ✅")


    if st.button("Generate Study Material"):


        with st.spinner("AI is preparing your study material..."):


            prompt = f"""

You are AI StudyMate.

Create:

1. Simple summary notes
2. Important exam points
3. Flashcards with Question and Answer
4. 10 quiz questions with answers
5. Revision plan


Study Material:

{text}

"""


            response = client.chat.completions.create(

                model="llama-3.1-8b-instant",

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                max_tokens=1500
            )


            st.subheader("📖 AI Generated Study Material")


            st.write(
                response.choices[0].message.content
            )