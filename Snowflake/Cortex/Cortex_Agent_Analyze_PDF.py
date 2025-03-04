# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.core import Root
from snowflake.cortex import Complete

MODELS = [
    "mistral-large2",
    "llama3.1-70b",
    "llama3.1-8b",
]


def init_messages():
    if st.session_state.clear_conversation or "messages" not in st.session_state:
        st.session_state.messages = []

def init_service_metadata():
    if "service_metadata" not in st.session_state:
        services = session.sql("SHOW CORTEX SEARCH SERVICES").collect()
        service_metadata = []
        if services:
            for srv in services:
                srv_name = srv["name"]
                srv_columns = session.sql(f"DESC CORTEX SEARCH SERVICE {srv_name}").collect()[0]["search_column"]
                service_metadata.append({"name": srv_name, "search_column": srv_columns})
        st.session_state.service_metadata = service_metadata

def init_config_options():
    with st.sidebar:
        st.selectbox("Select cortex search service:",[s["name"] for s in st.session_state.service_metadata], key="selected_cortex_search_service",)
        st.button("Clear Conversation", key="clear_conversation")
        st.toggle("Debug", key="debug", value=False)
        st.toggle("Use Chat History", key="use_chat_history", value=True)

        with st.expander("Advanced Options"):
            st.selectbox("Select the Model", MODELS, key="model_name")
            st.number_input("Select Number of Context Chunks", value=5, key="num_retrieved_chunks", min_value= 1, max_value= 10)
            st.number_input("Select Number of messages to be use in chat history", value= 5, key="num_chat_messages", min_value=  1, max_value= 10)

        st.expander("Session State").write(st.session_state)

def get_chat_history():
    start_index = max(0, len(st.session_state.messages) - st.session_state.num_chat_messages)
    return st.session_state.messages[start_index:len(st.session_state.messages)-1]

def complete(prompt: str):
    response = Complete(model = st.session_state.model_name, prompt= prompt)
    return response.replace("$", "\$")

def make_chat_history_summary(chat_history, question):
    prompt = f"""
    [INST]
    Based on the chat history below and the question, generate a query that extend the question
        with the chat history provided. The query should be in natural language.
        Answer with only the query. Do not add any explanation.

        <chat_history>
        {chat_history}
        </chat_history>
        <question>
        {question}
        </question>
    [/INST]
    """
    summary = complete(prompt)

    if st.session_state.debug:
        st.sidebar.text_area("Chat history Summary", summary, height=150)

    return summary

def query_cortex_search_service(query, columns= [], filter= {}):
    db, schema = session.get_current_database(), session.get_current_schema()
 
    cortex_search_service = (
        root.databases[db]
        .schemas[schema]
        .cortex_search_services[st.session_state.selected_cortex_search_service]
    )
    cortex_document = cortex_search_service.search(query, columns, filter, limit = st.session_state.num_retrieved_chunks)
    result = cortex_document.results

    service_metadata = st.session_state.service_metadata
    search_col = [s["search_column"] for s in service_metadata
                 if s["name"] == st.session_state.selected_cortex_search_service][0].lower()

    context_str = ""
    for i,r in enumerate(result):
        context_str += f"Context Document {i+1}: {r[search_col]}\n" + "\n"

    st.sidebar.text_area("Context Document", context_str, height= 500)
    return context_str, result


def create_prompt(question: str):
    if st.session_state.use_chat_history:
        chat_history = get_chat_history()
        if chat_history != []:
            question_summary = make_chat_history_summary(chat_history, question)
            context_str, result = query_cortex_search_service(question_summary, 
                                       columns=["chunks", "file_url", "relative_path"],
                                       filter={"@and": [{"@eq": {"language": "English"}}]},)
        else:
            context_str, result = query_cortex_search_service(question, 
                                       columns=["chunks", "file_url", "relative_path"],
                                       filter={"@and": [{"@eq": {"language": "English"}}]},)
    else:
        context_str, result = query_cortex_search_service(question, 
                                       columns=["chunks", "file_url", "relative_path"],
                                       filter={"@and": [{"@eq": {"language": "English"}}]},)
        chat_history = ""

    prompt = f"""
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
    return prompt, result

# Get the current credentials
session = get_active_session()

def main():
    st.title(f":speech_balloon: Chatbot with Snowflake Cortex")
    init_service_metadata()
    init_config_options()
    init_messages()

    icons = {"assistant": "❄️", "user": "👤"}

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=icons[message["role"]]):
            st.markdown(message["content"])

    disable_chat = (
        "service_metadata" not in st.session_state or
        len(st.session_state.service_metadata) == 0
    )

    if question := st.chat_input("What is your Question?"):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user", avatar=icons["user"]):
            st.markdown(question.replace("$", "\$"))

        with st.chat_message("assistant", avatar=icons["assistant"]):
            message_placeholder = st.empty()
            with st.spinner("Thinking..."):
                question = question.replace("'", "")
                prompt, result = create_prompt(question)
                generate_response = complete(prompt)
                markdown_table = "###### References \n\n| PDF Title | URL |\n|-------|-----|\n"
                for res in result:
                    markdown_table += f"| {res['relative_path']} | [LINK]({res['file_url']}) |\n"
                message_placeholder.markdown(generate_response + "\n\n" + markdown_table)
        st.session_state.messages.append(
            {"role": "assistant", "content": generate_response}
        )
    
    
if __name__ == "__main__":
    session = get_active_session()
    root = Root(session)
    main()
