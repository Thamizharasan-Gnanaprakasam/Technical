# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from datetime import datetime, timedelta, date
from snowflake.snowpark.functions import col, min, max, not_, upper
import numpy as np
import pandas as pd
from snowflake import snowpark
import json
import uuid
import io
import zipfile
from snowflake.cortex import Complete
import _snowflake
import sys




 



st.set_page_config(layout="wide")

st.session_state["green_color"] = "#0E5447"
st.session_state["white_color"] = "#fbf9f4"
st.session_state["orange_color"] = "#ff7540"

st.session_state["togg_def"] = "#BDC4D566"
st.session_state["toggle_color"] = st.session_state["togg_def"]
st.session_state["indx"] = 0
st.session_state["db"] = "SFT"
st.session_state["schema"] = "GTR_OPS_STATS"

st.session_state["data_center"] = ""
st.session_state["data_source"] = ""







if 'current_page' not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "curr_page" not in st.session_state:
    st.session_state.curr_page = "Dashboard"


# Write directly to the app
#st.sidebar.subheader("GTR Search")


head= st.container(key="head")
with head:
    row = st.columns(2)
    row[0].title(st.session_state.curr_page)
    hist_toggle = row[1].toggle("Preserve Search", key="toggle")

if hist_toggle:
    st.session_state["toggle_color"] = st.session_state["orange_color"]
else:
    st.session_state["toggle_color"] = st.session_state["togg_def"]

if "download_data" not in st.session_state:
    st.session_state["download_data"] = None










# Get the current credentials
session = get_active_session()
var_usr_nm = st.experimental_user["user_name"]

interpretation_prompt = """
You're an AI Assistant tasked with helping an analyst by interpreting retrieve data as a response to the analyst's question.
You will receive the analyst's question and the data retrieved to answer the question.
Concisely response to the analyst's question based on the data retrieved.
Be concise and only response for the isolated question and data retrieved.
Do not preface your response with anything besides the interpretation.

[Analyst Question]
{question}

[The Start of the Data Retrieved]
{data}
[The End of the Data Retrieved]
"""



def switch_page(page:str):
    st.session_state.current_page = page
    st.session_state.messages = []
    st.session_state.curr_page = page

def update_search_hist(start_date, end_date):
    try:
        user_check = session.sql(f"SELECT COUNT(1) FROM {st.session_state['db']}.{st.session_state['schema']}.USER_STREAMLIT_SEARCH WHERE USER_ID = '" + var_usr_nm + "'").collect()[0][0]
        
        
        if user_check == 0:
            var_sql = f"""INSERT INTO {st.session_state["db"]}.{st.session_state["schema"]}.USER_STREAMLIT_SEARCH (USER_ID ,START_DATE ,END_DATE ,DATA_CENTER ,DATA_SOURCE, FILTER_DATA ,COL_LIST ,REC_LMT ,CREATED_BY ,CREATED_AT  ) 
    SELECT '{var_usr_nm}','{str(start_date)}','{str(end_date)}','{data_cntr}','{data_source}',{rows_collection},$${str(cols_select).replace("[","").replace("]", "").replace("'","")}$$,{limit_no}
    ,'{var_usr_nm}',CURRENT_TIMESTAMP() from dual"""
        else:
            var_sql = f"""UPDATE {st.session_state["db"]}.{st.session_state["schema"]}.USER_STREAMLIT_SEARCH SET START_DATE = '{str(start_date)}', END_DATE = '{str(end_date)}', DATA_CENTER='{data_cntr}'
, DATA_SOURCE='{data_source}', FILTER_DATA = {rows_collection}, 
COL_LIST=$${str(cols_select).replace("[","").replace("]", "").replace("'","")}$$, REC_LMT = {limit_no}
  WHERE USER_ID ='{var_usr_nm}'"""
        
        session.sql(var_sql).collect()
    except Exception as e:
        st.text(var_sql)
        st.session_state["result_set"].error(str(e))

def download_full_file():
    #df = pd.DataFrame()
    
    file_name: str = f'{data_cntr.replace(" ","_")}_{data_source.replace(" ","_")}.csv.gz'
  
    download_df = session.create_dataframe(st.session_state["data_set"]["Data_Select"])
    
    #df.write.copy_into_location(f"@INT_STAGE/{file_name}", single= True, OVERWRITE = True, file_format_type="CSV", format_type_options={"COMPRESSION": "GZIP"})
    download_df.write.copy_into_location(f"@SFT.SFTR_STG.INT_STAGE/{file_name}", single= True, OVERWRITE = True, file_format_type="CSV", format_type_options={"COMPRESSION": "GZIP"})
    output = session.file.get(f"@SFT.SFTR_STG.INT_STAGE/{file_name}",fr"C:/Users/tganapra/Downloads/streamlit/{file_name}")
    st.text(output)

@st.dialog("Full Data Download")
def zip_df(file_name: str):
    if st.session_state["download_data"] == None:
        with st.spinner("Preparing Data for Download"):
            csv_string = st.session_state["data_set"]["Data_Select"].to_csv(index=False).encode("utf-8")
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr(f"{file_name}.csv", csv_string)
        
            buffer.seek(0)
            st.session_state["download_data"] = buffer.read()
    
    st.download_button("Start Download",st.session_state["download_data"] ,fr"{file_name}.zip", "application/zip", key='download-zip')
    return None

    
 
    
#@st.cache_data
def extract_data(_df: snowpark.DataFrame , start_date, end_date, col_list, limit_no = 0):
    #result_set = result_empty.container()
    st.session_state["download_data"] = None
    data_set = _df.filter((col(st.session_state["var_rpt_dt"])>=start_date) & (col(st.session_state["var_rpt_dt"])<=end_date))
    st.session_state["result_set"] = st.container()
    
    if len(rows_collection) > 0:
        for row in rows_collection:
            add_fltr_fld = row["name"]
            add_fltr_cnd = row["cond"]
            add_fltr_val = row["val"]
            if add_fltr_fld != "" and add_fltr_fld != None and add_fltr_val != "" :
                add_fltr_val_lst = [i.upper().strip() for i in add_fltr_val.split(";")]
                var_col = str(st.session_state["col_dict"].get(add_fltr_fld)).upper()
                if add_fltr_cnd == "EQUALS":
                    data_set = data_set.filter(upper(col(var_col)).in_(add_fltr_val_lst))
                else:
                    data_set = data_set.filter(~(upper(col(var_col)).in_(add_fltr_val_lst)))
            
            
    

    data_select = data_set.select(col_list)
    
    #data_set = df.select(col_list).filter(dt_fltr)
    if limit_no > 0:
        data_select = data_select.limit(limit_no)

    

    col_dict_rev = {v:k  for k,v in st.session_state["col_dict"].items()}
    
    disp_col = {col.upper(): col_dict_rev.get(col) for col in col_list}
    


    data_select_pd = data_select.to_pandas()

    data_select_pd.rename(columns = disp_col, inplace= True)
    #page_size = 10 
    st.session_state["data_set"] = {"Data_Select": data_select_pd, "chart_data": data_set.group_by(st.session_state["var_rpt_dt"]).count().select(st.session_state["var_rpt_dt"], col('COUNT').as_("UNQIUE_ID"))}
    st.session_state["last_page"]= len(data_select_pd) // st.session_state["page_size"]
    if st.session_state["last_page"] < 1:
        st.session_state["last_page"] = 1
    #st.session_state["chart_data"] = data_set.group_by(var_rpt_dt).count().select(var_rpt_dt, col('COUNT').as_("UNQIUE_ID"))

    

    #display_data_set(result_set, data_select_pd, data_set)

    
    if hist_toggle:
        update_search_hist(start_date,  end_date)
    #file_name: str = f'{data_cntr.replace(" ","_").upper()}_{data_source.replace(" ","_").upper()}'
    #st.session_state["zip_data"]  = zip_df(file_name)



def display_data(page_size = 50):
    st.session_state["result_set"].title("Result Set")
    data_res, count_chart = st.session_state["result_set"].tabs(["Data Set", "Count Chart"])
    with data_res:
        page_size = st.session_state["page_size"]
        last_pg = st.session_state["last_page"]
        sub_cont = data_res.container(key="data_set_cont")
        row = sub_cont.columns(4)
        row[0].empty()
        page_number = row[1].number_input("Page Number",min_value=1, max_value=last_pg, value=1, key="pg_nav", label_visibility='collapsed')
        row[2].text(f"/{last_pg} Pages")
        #row[3].button("Download Full File", key = uuid.uuid4(), on_click=download_full_file)
        file_name: str = f'{data_cntr.replace(" ","_").upper()}_{data_source.replace(" ","_").upper()}'
        #csv = st.session_state["data_set"]["Data_Select"].to_csv(index=False).encode('utf-8')
        #row[3].download_button("Download Full File",csv ,fr"{file_name}.csv", "text/csv", key='download-csv')
        #zip_data  = zip_df(file_name)
        row[3].button("Download Full File", key = "Download_file", on_click= zip_df, args= (file_name,))
        #row[3].download_button("Download Full File",st.session_state["zip_data"] ,fr"{file_name}.zip", "application/zip", key='download-zip')
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size

        data_res.dataframe(st.session_state["data_set"]["Data_Select"][start_index:end_index])
        #data_res.button("Download Full File", key = uuid.uuid4())

        
    with count_chart:
        count_chart.bar_chart(st.session_state["data_set"]["chart_data"], x= st.session_state["var_rpt_dt"], y="UNQIUE_ID" )
 

def get_index(data_res, data_select_pd, page_number, page_size):
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    data_res.dataframe(data_select_pd[start_index:end_index])

def get_hist_search():
    
    hist_data_raw = session.sql(f"SELECT START_DATE, END_DATE, DATA_CENTER, DATA_SOURCE, FILTER_DATA, COL_LIST, REC_LMT FROM {st.session_state['db']}.{st.session_state['schema']}.USER_STREAMLIT_SEARCH WHERE USER_ID = '{var_usr_nm}'").collect()
    if hist_data_raw !=[]:
        hist_data = hist_data_raw[0]
        return hist_data
    else:
        return [date.today(), date.today(), None, None, "[]", None, 0]
    
def add_row(fld_name = "", cnd = "", val = ""):
    element_id = uuid.uuid4()
    st.session_state["rows"][str(element_id)]=[fld_name, cnd, val]

def remove_row(row_id):
    st.session_state["rows"].pop(str(row_id))
    
def add_filter( fld: list, row_id, fld_name, cnd, val):
    fld_indx = fld.index(fld_name) if fld_name != '' else None
    cnd_indx = ["EQUALS","NOT EQUALS"].index(cnd) if cnd != '' else 0
    row_container = st.empty()
    row = row_container.columns(4)

    add_fltr_fld = row[0].selectbox("Column Name:", fld, index=fld_indx, key=f"add_fld_{row_id}")
    add_fltr_cnd = row[1].selectbox("", ["EQUALS","NOT EQUALS"], index=cnd_indx , key=f"add_con_{row_id}")
    add_fltr_val = row[2].text_input("Value:",val , key=f"val_{row_id}")
    if len(st.session_state["rows"]) > 1:
        row[3].button(":wastebasket:", key = f"del_{row_id}", on_click=remove_row, args=[row_id])
    return {"name": add_fltr_fld, "cond": add_fltr_cnd, "val": add_fltr_val}

def reset_session_var(data_cntr, data_source = st.session_state["data_source"]):
    if st.session_state["data_center"] != data_cntr or st.session_state["data_source"] != data_source:
       
        colm_list = None
        rec_lmt = 0
        rows_collection = []
        st.session_state["rows"] = {}
        st.session_state["data_set"] = {}
        add_row()


if "rows" not in st.session_state:
    st.session_state["rows"] = {}
if "togg_val" not in st.session_state:
    st.session_state["togg_val"] = False
    add_row()
    

rows_collection = []

####GETTING SEARCH HISTROY FOR THE ROLE#####


if "data_set" not in st.session_state:
    st.session_state["data_set"]={}
if "last_page" not in st.session_state:
    st.session_state["last_page"]=1
if "page_size" not in st.session_state:
    st.session_state["page_size"]=50
if "page" not in st.session_state:
    st.session_state["page"]=1
if "active_suggestion" not in st.session_state:
    st.session_state.active_suggestion = None



start_dt = date.today()
end_dt = date.today()
data_center = None
data_source = None

colm_list = None
rec_lmt = 0




if hist_toggle:
    start_dt, end_dt, data_center, data_source, filter_data, colm_list, rec_lmt = get_hist_search()
    st.session_state["data_center"] = data_center
    st.session_state["data_source"] = data_source
    
    if not(st.session_state["togg_val"]):
        rows_collection = list(json.loads(filter_data))
        st.session_state["rows"] = {}
        st.session_state["togg_val"] = True
    
    if len(rows_collection) > 0 and st.session_state["rows"] == {}:
        for row in rows_collection:
            add_row(row["name"], row["cond"], row["val"])
else: 
    if st.session_state["togg_val"]:
        st.session_state["rows"] = {}
        st.session_state["togg_val"] = False
        

if st.session_state["rows"] == {}:
    add_row()


rows_collection = []
    



if colm_list == "" or colm_list is None:
    colm_list = None
else:
    colm_list = [col.strip() for col in colm_list.split(',')]

if "col_dict" not in st.session_state:
    st.session_state["col_dict"] = {}
if "var_rpt_dt" not in st.session_state:
    st.session_state["var_rpt_dt"] = ""
if "result_set" not in st.session_state:
    st.session_state["result_set"] = None



    
####GETTING DATA CENTER DETAILS FROM SF TABLE#####
dc_dtls = session.table(f'{st.session_state["db"]}.{st.session_state["schema"]}.STREAMLIT_DATA_CENTER')

dc_raw = dc_dtls.select(col('DATA_CENTER')).distinct(col('DATA_CENTER')).collect()
dc_list = [ row[0] for row in dc_raw]

if data_center != None:
    dc_index = dc_list.index(data_center)
else:
    dc_index = None

with st.sidebar:
    st.title("GTR Search")
    data_cntr = st.selectbox("Data Center:",dc_list, index=dc_index)
    
    ##GETTING DATA SOURCE###
    dc_dtls_fltr = dc_dtls.filter(col("DATA_CENTER") == data_cntr)
    ds_raw = dc_dtls_fltr.select(col('DATA_SOURCE')).distinct(col('DATA_SOURCE')).collect()
    ds_list = [ row[0] for row in ds_raw]
    
    if data_source != None:
        ds_index = ds_list.index(data_source)
    else:
        ds_index = None
    
    data_source = st.selectbox("Data Source:", ds_list, index=ds_index, on_change=reset_session_var, args=(data_cntr,))

    #st.button("Dashboard", key="dash", on_click=switch_page, args=('dashbrd',))
    #st.button("Chat Bot", key="chat", on_click=switch_page, args=('chat',))

if "messages" not in st.session_state:
    st.session_state.messages = []

#if "semantic_model" not  in st.session_state:
    
#    for indx, row in enumerate(dc_dtls.select(col('YAML_CONTENT')).distinct(col('YAML_CONTENT')).collect()):
#        if indx > 0:
#            lines = row[0].splitlines(keepends=True)
#            new_text = "".join(lines[3:])
#            st.session_state["semantic_model"] += new_text
#        else:
#            st.session_state["semantic_model"] = row[0]

if data_source != "" and data_source != None:
    st.session_state["semantic_model"] = dc_dtls_fltr.filter(col('DATA_SOURCE') == data_source).select(col('YAML_CONTENT')).collect()[0][0]
else:
    st.session_state["semantic_model"] = ""
   

def dashboard():
    st.session_state.messages = []
    try:
        
        
        filter_cont = st.container()
        
        
        with filter_cont:
            cols = st.columns(3)
            date_range = cols[0].date_input("Search period:", value=(start_dt, end_dt))
        
        
        
        
            
        ds_raw = dc_dtls_fltr.filter(col('DATA_SOURCE') == data_source).select(col('SRC_TBL'), col('COL_LIST'), col('RPT_DT_FLD_NAME') ).collect()
        data_src: str = ds_raw[0][0]
        st.session_state["col_dict"] = json.loads(ds_raw[0][1])
        
        st.session_state["var_rpt_dt"] = str(ds_raw[0][2]).upper()
    
     
    
        
    
        
    
        with filter_cont:
            with filter_cont.expander("Trade Filter"):

                fld: list = [key for key in st.session_state["col_dict"].keys()]
    
                
                
                for row in st.session_state["rows"].keys():
                    
                    row_data = add_filter(fld, row, *st.session_state["rows"].get(row))
                    
                    
                    if row_data["name"] != None and row_data["val"] != None:
                        rows_collection.append(row_data)
    
                
                st.button("Add Filter", on_click=add_row)
                st.text('Seperate Values by Semi-colon (;)')
                
            #add_fld_cont = filter_cont.container()
                
        
        
        
        sub_df = session.table(data_src)
    
    
        with filter_cont.expander("Output Columns"):
            cols = st.columns(2)
            cols_select = cols[0].multiselect("Available Columns", st.session_state["col_dict"].keys(),colm_list, key="col_select")
            limit_no = cols[1].number_input("Output Limit, 0 for No Limit",min_value=0, value=0, key="row_lmt")
        
        
        #var_rpt_dt = str(col_dict.get("Report Date")).upper()
        
        if cols_select == []:
            col_to_disp = list(st.session_state["col_dict"].values())
            #col_to_disp.remove("ALL")
        else:
            col_to_disp = [st.session_state["col_dict"].get(key) for key in cols_select]
    
        
        
        with filter_cont:
            
            try:
                filter_cont.button("Submit", on_click=extract_data, args=[sub_df, date_range[0], date_range[1], col_to_disp,int(limit_no)])
            except IndexError:
                filter_cont.button("Submit", on_click=extract_data, args=[sub_df, date_range[0], date_range[0], col_to_disp,int(limit_no)])
            except Exception as e:
                filter_cont.text(str(e))
        
        
    
    
        
        #st.text(len(st.session_state["chart_data"]))
        #result_empty = st.container()
        st.session_state["result_set"] = st.container(key="res_set")
    
        if st.session_state["data_set"] != {}:
            
            display_data()
           
    
    except IndexError as e:
        pass
    except Exception as e:
        st.text(str(e))
def send_message():
    request_body = {"messages": [st.session_state.messages[-1]]
                    #,"semantic_model_file": f"@{DATABASE}.{SCHEMA}.{STAGE}/{FILE}"
                    ,"semantic_model": st.session_state["semantic_model"],}
    
    #st.text(request_body)
    resp = _snowflake.send_snow_api_request(
                    "POST",
                    f"/api/v2/cortex/analyst/message",
                    {},
                    {},
                    request_body,
                    {},
                    30000,
                )
    return json.loads(resp["content"])


def process_msg(prompt: str):
    st.session_state.messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})
    with st.chat_message(st.session_state.messages[-1]["role"]):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Processing Data..."):
            response = send_message()
            content = response["message"]["content"]
            display_content(content)
    st.session_state.messages.append({"role": "assistant", "content": content})
            
def set_active_sugg(suggestion):
    st.session_state.active_suggestion = suggestion
    
def display_content(content):
    try:
 
        for item in content:
            if item["type"] == "text":
                st.markdown(item["text"])
                question = item["text"]
            if item["type"] == "sql":
                with st.expander("SQL", expanded=False):
                    st.code(item["statement"],"sql")
                df = session.sql(item["statement"]).to_pandas()
                df_size = sys.getsizeof(df)/1024/1024
                if df_size <= 43:
                    resp = Complete(model='llama3.1-8b', prompt = interpretation_prompt.format(question = question, data=df.to_dict(orient="records")), session= session)
                    ai, data, chart = st.tabs(["AI Response", "Data Set", "Chart"])
                    ai.markdown(resp)
                    data.dataframe(df)
                    chart.bar_chart(df, x=df.columns[0])
                else:
                    st.error(f"Sorry, Size of Data is More than 43 MB and I can't handle it. Above is the Query, please use Snow Sight to run this Query and get the Data Set or Use Dashboard")
            if item["type"] == "suggestions":
                with st.expander("Suggestions", expanded= True):
                    for suggesion in item["suggestions"]:
                        st.button(suggesion, key=str(uuid.uuid4()), on_click=set_active_sugg, args=(suggesion, ))
    except Exception as e:
        st.error(str(e))


def chatbot():
    st.session_state.messages = []
    if data_cntr != "" and data_source != "" and data_cntr != None and data_source != None:
        st.session_state.messages.append({"role": "assistant", "content":[{"type": "text", "text": "How may I assist you?"}]})
    else:
        st.session_state.messages.append({"role": "assistant", "content":[{"type": "text", "text": "Please Select Data Source to start the Conversation"}]})
    

fn_map= {
    'Dashboard':dashboard,
    'Chat Bot':chatbot
}

active_page = fn_map.get(st.session_state.current_page, dashboard)
if st.session_state.messages == []:
    active_page()


chatbot_head = st.container(key="chat_head")
if st.session_state.messages != []:
    for message in st.session_state.messages:
        with chatbot_head:
            with st.chat_message(message["role"]):
                
                display_content(message["content"])

if st.session_state.current_page == 'Dashboard':
    with st.sidebar:
        st.button("Switch to Chat Bot", key="chat", on_click=switch_page, args=('Chat Bot',))


    

if st.session_state.active_suggestion != "" and st.session_state.active_suggestion != None:
    with chatbot_head:
        process_msg(st.session_state.active_suggestion)
    st.session_state.active_suggestion = ""


if st.session_state.current_page == 'Chat Bot':
    chat_cont = st.container(key="chat_bot")
    with st.sidebar:
        st.button("Switch to Dashboard", key="dash", on_click=switch_page, args=('Dashboard',))
    if data_cntr != "" and data_source != "" and data_cntr != None and data_source != None:
        #with chat_cont:
        #st.subheader("Post your question")
            if prompt := st.chat_input(key="chat_bot_in"):
                with chatbot_head:
                    process_msg(prompt)                 
if st.session_state.current_page == 'Dashboard':
    bottom = st.container(key="foot")
    bottom.title("DTCC")



###CSS######
css = f""" 
h1{{ 
    color:{st.session_state["green_color"]}; 
    font-family:"Times New Roman",Times,serif; }} 
h2{{ 
    color:{st.session_state["green_color"]}; 
    font-family:"Times New Roman",Times,serif; }} 
h3{{ 
    color:{st.session_state["green_color"]}; 
    font-family:"Times New Roman",Times,serif; }} 
p{{ 
color:{st.session_state["green_color"]}; 
font-family:Arial,Arial,Helvetica,sans-serif; }} 

div[data-testid="stMainBlockContainer"]{{ 
    background-color:{st.session_state["white_color"]}; 
    }}
div.st-key-head p{{
#text-align: right;
#font-size: 12px;
}}
button[kind="secondary"]{{
background-color:{st.session_state["orange_color"]};
}}

div.st-key-foot h1{{
background-color:{st.session_state["green_color"]}; 
color:{st.session_state["white_color"]}; 
text-align: right;
font-family: "Lustra Black", "sans-serif";
}}
div[data-testid="stHeadingWithActionElements"].st-emotion-cache-m78myu e1nzilvr3 h1{{

color:{st.session_state["white_color"]}; 
}}



div.st-key-toggle > div > label[data-baseweb="checkbox"] >   div:nth-child(1)  {{
background-color:{st.session_state["toggle_color"]};
}}










div.st-key-pg_nav{{
width: 20px;
}}



div[data-baseweb="tab-highlight"]{{
background-color:{st.session_state["orange_color"]};
}}

div.st-key-pg_nav > div > div > div:nth-child(2) > button:inactive {{
background-color: {st.session_state["orange_color"]};
highlight-color: {st.session_state["orange_color"]};
}}

div.st-key-pg_nav > div > div > div:nth-child(2) > button:hover {{
background-color: {st.session_state["orange_color"]};
highlight-color: {st.session_state["orange_color"]};
}}

div.st-key-pg_nav > div > div > div:nth-child(2) > button:active {{
background-color: {st.session_state["orange_color"]};
highlight-color: {st.session_state["orange_color"]};
}}


div.st-key-row_lmt > div > div > div:nth-child(2) > button:inactive {{
background-color: {st.session_state["orange_color"]};
highlight-color: {st.session_state["orange_color"]};
}}

div.st-key-row_lmt > div > div > div:nth-child(2) > button:hover {{
background-color: {st.session_state["orange_color"]};
highlight-color: {st.session_state["orange_color"]};
}}

div.st-key-row_lmt > div > div > div:nth-child(2) > button:active {{
background-color: {st.session_state["orange_color"]};
highlight-color: {st.session_state["orange_color"]};
}}

div.st-key-col_select > div > div > div > div >div > span{{
background-color: {st.session_state["orange_color"]};
}}

div.st-key-data_set_cont > div > div > div > div > div > div > div > div {{
color: {st.session_state["green_color"]};
font-size: 25px;
}}



stApp{{ 
    background-color:{st.session_state["white_color"]}; 
    font-family:Arial,Arial,Helvetica,sans-serif; 
    }} 
div[data-testid="stAppViewBlockContainer"]{{ 
    background-color:{st.session_state["orange_color"]}; 
    }} 

svg[title="open"]:hover {{
background-color: {st.session_state["orange_color"]};
highlight-color: {st.session_state["orange_color"]};
}}

svg[data-testid="stExpanderToggleIcon"]:hover {{
stroke: {st.session_state["orange_color"]};
highlight-color: {st.session_state["orange_color"]};
}}

div[data-testid="stMainBlockContainer"] button[kind="secondary"] p{{ color:white; }}

div[data-testid="stSidebarContent"] {{
background-color: {st.session_state["green_color"]};
}}

div[data-testid="stSidebarContent"] p {{
color: {st.session_state["white_color"]};
}}

div[data-testid="stSidebarContent"] h3{{ 
    color:{st.session_state["white_color"]}; 
    font-family:"Times New Roman",Times,serif; }}

div[data-testid="stSidebarContent"] h1{{ 
    color:{st.session_state["white_color"]}; 
    font-family:"Times New Roman",Times,serif; }}

div[data-testid="stMarkdownContainer"] li {{
color: {st.session_state["green_color"]};
}}

div.chat_head {{
overflow: auto;
height: 70vh;
}}

div.head {{
hegiht: 100%;
}}

div[data-testid="stBottomBlockContainer"] {{
background-color: {st.session_state["white_color"]};
}}

section[data-testid="stAppScrollToBottomContainer"] > div:nth-child(2) {{
background-color: {st.session_state["white_color"]};
}}

 """ 

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)