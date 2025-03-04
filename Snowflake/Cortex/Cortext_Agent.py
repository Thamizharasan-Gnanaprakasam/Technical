# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.cortex import Complete
import _snowflake
import json
from typing import Union

session = get_active_session()

API_ENDPOINT = r'/api/v2/cortex/agent:run'
API_TIMEOUT = 50000 #IN MM


CORTEX_SEARCH_SERVICE = 'sales_intelligence.data.sales_conversation_search'
SEMANTIC_MODELS = '@sales_intelligence.data.models/sales_metrics_model.yaml'

def snowflake_api_call1(query: str):
    body = {"model": "llama3.1-8b",
        "messages":[{"role": "user",
                        "content": [
                            {"type": "text",
                            "text": query}
                        ]}],
           "semantic_model_file": SEMANTIC_MODELS}

    response = _snowflake.send_snow_api_request("POST",
                                               "/api/v2/cortex/agent:run",
                                               {},
                                               {},
                                               body,
                                               None,
                                               3000)
    st.text(json.loads(response["content"]))

    

def snowflake_api_call(query: str, limit: int = 10) :
    payload = {
        "model": "llama3.1-70b",
        "messages": [
            {"role": "user",
            "content": [
                {
                    "type": "text",
                "text": query
                }
            ]
            }
        ],
        "tools": [
            {
                "tool_spec": {
                    "type": "cortex_analyst_text_to_sql",
                    "name": "analyst1"
                }
            },
            {
                "tool_spec": {
                    "type": "cortex_search",
                    "name": "search1"
                }
            }
        ],
        "tool_resources": {
            "analyst1": {"semantic_model_file": SEMANTIC_MODELS},
            "search1": {
                "name": CORTEX_SEARCH_SERVICE,
                "max_result": limit
            }
        }
    }

    try:
        resp = _snowflake.send_snow_api_request(
            "POST", #METHOD
            API_ENDPOINT, #PATH
            {}, #HEADER
            {}, #PARAMS
            payload, # BODY
            None, # REQUEST_GUID
            API_TIMEOUT # TIMEOUT IN MM
        )
        try:
            resp_content = json.loads(resp["content"])
        except json.JSONDecodeError:
            st.error("❌ Failed to parse API response. The server may have returned an invalid JSON format.")

            if resp["status"] != 200:
                st.error(f"Error:{resp} ")
                return None

        return resp_content
    except Exception as e:
        st.error(f"Error making request: {str(e)}")  
        return None

def process_sse_response(response: json):
    text = ""
    sql = ""
    

    if not response:
        return text, sql

    try:
        for event in response:
            if event.get("event") == "message.delta":
                data = event.get("data", {})
                delta = data.get("delta", {})

                for content in delta.get("content",[]):
                    content_type = content.get("type")
                    if content_type == "tool_results":
                        tool_results = content.get("tool_results",{})
                        if "content" in tool_results:
                            for results in tool_results.get("content",[]):
                                if results.get("type") == "json":
                                    json_content = results.get("json")
                                    text += f"\n{json_content.get('text','')}"
                                    for suggestion in json_content.get("suggestions",[]):
                                        text += f"\n• {suggestion}"
                                    for search_result in json_content.get('searchResults',[]):
                                        text += f"\n• {search_result.get('text', '')}"
                                    
                                    sql = json_content.get("sql")
                    if content_type == "text":
                        text += content.get("text","")
                    
    except json.JSONDecodeError as e:
        st.error(f"Error processing events: {str(e)}")
    except Exception as e:
        st.error(f"Error processing events: {str(e)}")
    return text,sql

def main():
    st.title("Intelligent Sales Assistant")

    with st.sidebar:
        if st.button("New Conversation", key="new_chat"):
            st.session_state.messages = []
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if query := st.chat_input("Would you like to Learn?"):
        with st.chat_message("user"):
            st.markdown(query)

        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("assistant"):
            with st.spinner("Processing your Request...."):
                snowflake_api_call1(query)
                response =snowflake_api_call(query, 1)
                st.text(response)
                text, sql = process_sse_response(response)
            if text:
                st.text(text)
                st.session_state.messages.append({"role": "assistant", "content": text})
            if sql:
                with st.expander("SQL", expanded=False):
                    st.code(sql, language="sql")
                df = session.sql(sql).to_pandas()
                st.dataframe(df)

if __name__ == '__main__':
    main()