# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import pandas as pd
import json
import re
from snowflake.cortex import Complete


st.set_page_config(page_title=":dolphin:  ABC",
                  initial_sidebar_state="expanded")

MODEL_PARAMS = {
    'temperature': {'min': 0.01, 'max': 1.0, 'default': 0.7, 'step': 0.01},
    'top_p': {'min': 0.01, 'max': 1.0, 'default': 1.0, 'step': 0.01},
    'max_tokens': {'min': 10, 'max': 100, 'default': 20, 'step': 10},
    'presence_penalty': {'min': -1.0, 'max': 1.0, 'default':0.0, 'step': 0.1},
    'frequency_penalty': {'min': -1.0, 'max': 1.0, 'default':0.0, 'step': 0.1},
}




# Get the current credentials
session = get_active_session()

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

def escape_sql_string(s: str):
    return s.replace("'", "''")

def extract_think_content(response):
    #st.text(response)
    think_pattern = r'<think>(.*?)</think>'
    think_match = re.search(think_pattern, response,re.DOTALL)
    

    if think_match:
        think_content = think_match.group(1).strip()
        main_response = re.sub(think_pattern, '', response, flags=re.DOTALL).strip()
        return think_content, main_response

    return None, response
    

def generate_deepseek_response(prompt, **params):
    string_dialogue ="".join(
        f"{msg['content']}\n\n"
        for msg in st.session_state.messages
    )

    ##st.text(string_dialogue)
    

    cortex_prompt = f"'[INST] {string_dialogue}{prompt} [/INST]'"
    prompt_data = [{"role": "user", "content": cortex_prompt}], params
    #st.text(json.dumps(prompt_data))
    prompt_json = escape_sql_string(json.dumps(prompt_data))
    
    #response = session.sql("select snowflake.cortex.complete(?, ?)", 
    #                      params=['llama3.1-8b', prompt_json]).collect()
    #response = Complete('llama3.1-8b', f"one line DESCRIBE with 'DESC:' word in front and list down with serial number the synonyms with header as 'SYNO' and 'END SYNO' at end of list for field {prompt} IN TABLE SFT.SFTR_DW.SUBMISSION_SFT_TRADE_DTLS_VW")
    #response = Complete('llama3.1-8b', f"One line Description about TABLE SFT.SFTR_DW.SUBMISSION_SFT_TRADE_DTLS_VW with 'DESC:' word in front")
    #response = Complete('llama3.1-8b', prompt_json)
    response = Complete('llama3.1-8b', prompt_json)

    #st.text(response)
    
    #st.text([data for data in response.split("**") if not(data.__contains__("\n"))])
    #st.text(prompt_data)
    #st.text(prompt_json)
    return response
    


with st.sidebar:
    st.title(":whale::speech_balloon:  DeepSeek R1 Chatbot")
    st.text("This chatbot is created using the DeepSeek R1 LLM model via Snowflake Cortex.")

    st.subheader(":gear: Model Parameters")
    params = {param: st.slider(param.replace("_"," ").title(),
                              min_value=settings["min"],
                              max_value = settings["max"],
                              value = settings["default"],
                              step = settings["step"]) for param, settings in MODEL_PARAMS.items()}
    st.button("Clear Chat", on_click= clear_chat_history)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input():
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            status_contanier =st.status("Thinking", expanded=True)

        with status_contanier:
            response = generate_deepseek_response(prompt, **params )
            think_content, main_response = extract_think_content(response)
            #if think_content:
            #    st.write(think_content)

        status_contanier.update(label="Thoughts", state = "complete", expanded= False)
        st.markdown(main_response)
        st.session_state.messages.append(({"role": "assistant", "content": main_response}))
        