# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import PyPDF2
from snowflake.cortex import Complete
import io
from docx import Document
import subprocess
import os




AI_prompt = """
            [INST]
            You are a helpful AI chat assistant with RAG capabilities. When a user asks you a question,
            you will also be given context provided between <context> and </context> tags. Use that context
            with the user's chat history provided in the between <chat_history> and </chat_history> tags
            to provide a summary that addresses the user's question. Ensure the answer is coherent, concise,
            and directly relevant to the user's question.

            If the user asks a generic question which cannot be answered with the given context or chat_history,
            just say "I don't know the answer to that question.

            Don't saying things like "according to the provided context".

            <chat_history>
            {chat_history}
            </chat_history>
            <context>
            {context_str}
            </context>
            <question>
            {question}
            </question>
            [/INST]
            Answer:
            """
# Write directly to the app
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_cont" not in st.session_state:
    st.session_state.pdf_cont = ""


# Get the current credentials
session = get_active_session()

def process_prompt(prompt: str):
    question = {"role": "user", "content": prompt}
    with st.chat_message(question["role"]):
        st.markdown(question["content"])
    st.session_state.messages.append(question)
    with st.chat_message("assistant"):
        with st.spinner("Processing....."):
            resp = Complete(model= "llama3.1-8b",
                           prompt = AI_prompt.format(chat_history= st.session_state.messages,
                                                    context_str= st.session_state.pdf_cont,
                                                    question= question),
                           session = session)
        st.markdown(resp)
    st.session_state.messages.append({"role": "assistant", "content": resp})

def read_pdf():
    data = PyPDF2.PdfReader(st.session_state.file)
    st.session_state.pdf_cont = ""
    for page in data.pages:
        st.session_state.pdf_cont += " " + page.extract_text().replace('\n',' ').replace('\0', ' ')
        
def read_doc():
    doc = Document(st.session_state.file)
    st.session_state.pdf_cont = ""
    for para in doc.paragraphs:
        st.session_state.pdf_cont += " " + para.text.replace("\n"," ").replace("\0"," ")

def read_txt():
    data = st.session_state.file.getvalue().decode("utf-8")
    st.session_state.pdf_cont = data.replace("\n", " ").replace("\0", " ")
    

st.title("PDF Reader")
st.sidebar.file_uploader("Upload File", key="file", type=["pdf", "docx", "txt"])
#st.text(io.StringIO(a.getvalue()))




if st.session_state.file != None:
    if st.session_state.file.name.split(".")[-1] == "pdf":
        read_pdf()
    if st.session_state.file.name.split(".")[-1] == "docx":
        read_doc()
    if st.session_state.file.name.split(".")[-1] == "txt":
        read_txt()
    
st.sidebar.write(st.session_state)
if st.session_state.messages != []:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
if prompt := st.chat_input(key="chat_inp"):
    process_prompt(prompt)

