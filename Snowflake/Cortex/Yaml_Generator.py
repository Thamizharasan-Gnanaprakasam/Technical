# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
import yaml
from snowflake.snowpark.functions import col
from snowflake.cortex import Complete
from time import perf_counter
import re


# Get the current credentials
session = get_active_session()
st.set_page_config(layout="wide")
#schema = ""
#table = ""
output = ""
streamlit_tbl = 'SFT.GTR_OPS_STATS.STREAMLIT_DATA_CENTER'
yaml_tbl = {}

if "main_window" not in st.session_state:
    st.session_state.main_window = st.container(key="main_win")
bottom = st.container(key="bottom")


if "final_tbl_data" not in st.session_state:
    st.session_state["final_tbl_data"] = []

if "yaml_tbl" not in st.session_state:
    st.session_state.yaml_tbl={}

st.session_state["sql"] = ""
st.session_state["disabled"] = False

st.session_state["green_color"] = "#0E5447"
st.session_state["white_color"] = "#fbf9f4"
st.session_state["orange_color"] = "#ff7540"

if "db" not in st.session_state:
    st.session_state["db"] = ""
if "schema" not in st.session_state:
    st.session_state["schema"] = ""
if "table" not in st.session_state:
    st.session_state.table = []

pattern = r"^[0-9]+\. (.*)$"
col_match = re.compile(pattern)
#desc_pattern = r"^\*{0,2}DESC:\*{0,2} (.*)$"
desc_pattern = r"^`{0,1}\*{0,2}DESC:\*{0,2} ([A-Za-z0-9\.\(\) -:_`]*)`{0,1}$"
desc_match = re.compile(desc_pattern)

def fetch_database():
    databases = session.sql("SHOW DATABASES").collect()
    for db in databases:
        st.session_state["database"].append(db["name"])

def fetch_schema(db: str):
    st.session_state["schemas"] = []
    schemas = session.sql(f"SHOW SCHEMAS IN DATABASE {db}").collect()
    
    for schema in schemas:
        st.session_state["schemas"].append(schema["name"])

def fetch_table(db: str, schema: str):
    st.session_state["tables"] = []
    df_tbl = session.table(f"{db}.INFORMATION_SCHEMA.TABLES")
    df_tbl = df_tbl.filter((col('TABLE_CATALOG') == db) & (col('TABLE_SCHEMA') == schema) & (col('TABLE_TYPE').in_(['VIEW','BASE TABLE']))  ).select(col('TABLE_NAME')).collect()
    st.session_state["tables"] = [row[0]  for row in df_tbl]

def run_complete(prompt, model='llama3.1-8b', session= session):
    return Complete(model= model, prompt= prompt, session= session)

    
def build_metadata(db: str, schema: str, tables: str):
    st.session_state.main_window = st.container(key="main_win")
    st.session_state.yaml_tbl = {"name": "SFTR Tables",
               "description": 'SFTR Tables that shows Submission, Outstanding Positions and Recon Data',
               "tables": []}
    for table in tables:

        
        v_sql = f"""
        SELECT LISTAGG(COLUMN_NAME,',')
        FROM information_schema.columns
        WHERE table_schema = '{schema}'
        AND table_catalog = '{db}'
        AND table_name = '{table}'"""
    
        col_list = session.sql(v_sql).collect()[0][0]
    
        v_sql = f"""
        SELECT DATA_SOURCE
        FROM {streamlit_tbl}
        WHERE SRC_TBL ILIKE '%{table}'
        """
        data_src = session.sql(v_sql).collect()
        if data_src != []: 
            data_src = data_src[0][0]
            st.session_state["disabled"] = False
        else:
            data_src = table
            st.session_state["disabled"] = True
        
        v_sql = f"""
        SELECT  'WITH TBL AS (SELECT ' || LISTAGG('LISTAGG(' || COLUMN_NAME || ',''%:|'') || '':;:'' ||
    REPLACE(REPLACE(SNOWFLAKE.CORTEX.COMPLETE(''llama3.1-8b'',''LIST DOWN SYNONYMS FOR TABLE FIELD ' || COLUMN_NAME || ''' ),''"'',''''),'','','''') AS ' || COLUMN_NAME , ',') || ' 
        FROM {db}.{schema}.{table} TABLESAMPLE ROW(10 ROWS)), SAMPLE_DATA AS (SELECT 
        COLUMN_NAME,
        VALUE
        FROM TBL
        UNPIVOT(VALUE FOR COLUMN_NAME IN ({col_list})) AS unpivoted_data)
        SELECT
        ARRAY_CONSTRUCT(
        
        table_name,
        '''' ,
        table_catalog ,
        table_schema ,
        A.column_name,
        data_type,
        is_nullable,
       B.VALUE
       ,''{data_src}''
       )
       FROM {db}.information_schema.columns A
        INNER JOIN SAMPLE_DATA B
        ON A.COLUMN_NAME = B.COLUMN_NAME
        WHERE table_schema = ''{schema}''
        AND table_catalog = ''{db}''
        AND table_name = ''{table}'''
        FROM information_schema.columns
        WHERE table_schema = '{schema}'
        AND table_catalog = '{db}'
        AND table_name = '{table}';
        """
    
        v_sql = f"""
        SELECT  'WITH TBL AS (SELECT ' || LISTAGG('LISTAGG(' || COLUMN_NAME || ',''%:|'')  AS ' || COLUMN_NAME , ',') || ' 
        FROM {db}.{schema}.{table} TABLESAMPLE ROW(10 ROWS)), SAMPLE_DATA AS (SELECT 
        COLUMN_NAME,
        VALUE
        FROM TBL
        UNPIVOT(VALUE FOR COLUMN_NAME IN ({col_list})) AS unpivoted_data)
        SELECT
        ARRAY_CONSTRUCT(
        
        table_name,
        '''' ,
        table_catalog ,
        table_schema ,
        A.column_name,
        data_type,
        is_nullable,
       B.VALUE
       ,''{data_src}''
       )
       FROM {db}.information_schema.columns A
        INNER JOIN SAMPLE_DATA B
        ON A.COLUMN_NAME = B.COLUMN_NAME
        WHERE table_schema = ''{schema}''
        AND table_catalog = ''{db}''
        AND table_name = ''{table}'''
        FROM information_schema.columns
        WHERE table_schema = '{schema}'
        AND table_catalog = '{db}'
        AND table_name = '{table}';
        """
        
        with st.session_state.main_window:
            #st.session_state["start"] = perf_counter()
            with st.spinner("Running SQL..."):
                st.session_state["sql"] = session.sql(v_sql).collect()[0][0]
                sample_data = session.sql(st.session_state["sql"]).collect()
                
                st.session_state["final_tbl_data"] = [row[0].replace("'","").replace("[","").replace("]","").replace('"','').replace("\n","").split(',') for row in sample_data]
            
        st.session_state["sql"] = ""
        generate_yaml(st.session_state["final_tbl_data"])
    
    


def generate_yaml(table_data):
    #st.session_state.main_window = st.container(key="main_win")
    
    for indx, row in enumerate(table_data):
        synonyms = []
        col_desc = ""
        tbl_desc = ""
        syn_indx = 0
        #st.text(len(row))
        table_name = row[0].strip()
        table_desc = row[1].strip()
        db = row[2].strip()
        schema = row[3].strip()
        column_name = row[4].strip()
        data_type = row[5].strip()
        is_nullable = row[6].strip()
        sample_data = row[7].split(':;:')[0].strip()
        #st.text(row[7].split(':,:')[1])
        name = row[8].strip()
        with st.session_state.main_window:
            with st.spinner(f"Getting Synonyms for Columns {indx+1} of {len(table_data)}"):
                syno_concat= run_complete(prompt=f"one line DESCRIBE with 'DESC:' word in front and list down with serial number the synonyms with header as 'SYNO' and 'END SYNO' at end of list for field {column_name} IN TABLE {db}.{schema}.{table_name}")
                #syno_concat = Complete(model='llama3.1-8b', prompt=f"one line DESCRIBE with 'DESC:' word in front and list down with serial number the synonyms with header as 'SYNO' and 'END SYNO' at end of list for field {column_name} IN TABLE {db}.{schema}.{table_name}", session= session)
        #syno_concat = row[7].split(':;:')[1].strip() if row[7].__contains__(':;:') else []
        #st.text(perf_counter() - st.session_state["start"])


        for row in syno_concat.split("\n"):
            #st.text(row)
            #st.text(syn_indx)
            if row.__contains__("END SYNO"):
                syn_indx = 0
            if row.__contains__("DESC:"):
                col_desc = desc_match.match(row).group(1)
            #st.text(col_match.match(row))
            if syn_indx == 1 and col_match.match(row):
                synonyms.append(str(col_match.match(row).group(1)).replace("*","").replace("`","").strip())
            #st.text(col_desc)
            if row.__contains__("SYNO"):
                syn_indx = 1

        
        if synonyms == []:
            synonyms = [' ']
        #st.text(synonyms)
        flg = 0
        for tbl in st.session_state.yaml_tbl["tables"]:
            if tbl["name"] == table_name:
                flg = 1
                column_list = tbl['dimensions']
                break

        if flg == 0:
                
        #if 'tables' not in yaml_tbl:
            file_name = table_name
            with st.session_state.main_window:
                with st.spinner(f"Getting Description for Table {db}.{schema}.{table_name}"):
                    response = run_complete(prompt= f"One line Description about TABLE {db}.{schema}.{table_name} and put DESC in front of the description")
            for row in response.split("\n"):
                #st.text(row)
                if desc_match.match(row):
                    #st.text("called")
                    #st.text(desc_match.match(row).group(1))
                    tbl_desc = str(desc_match.match(row).group(1)).replace("*","").replace("`","").strip()
                
           
            st.session_state.yaml_tbl["tables"].append({'name': table_name,
                                    'description': tbl_desc,
                                      'base_table': {
                                    'database': db,
                                    'schema': schema,
                                      'table': table_name},
                                    'dimensions': []
                                    })
            column_list = st.session_state.yaml_tbl['tables'][-1]['dimensions']

        column_list.append({
                                        'name': column_name,
                                        'synonyms': synonyms,
                                        'description': col_desc,
                                        'expr': column_name,
                                        'data_type': data_type,
                                        'unique': False,
                                        'sample_values': list({val for val in sample_data.split('%:|')})
                                    })

    


    #with open('snowflake.yaml', 'w') as f:
    
            #st.text_area('',output)

@st.dialog("YAML Update")
def update_streamlit(yaml_data, table):
    with st.spinner("Updating Table...."):
        v_sql=f"""
        UPDATE {streamlit_tbl}
        SET YAML_CONTENT = $${yaml_data}$$
        WHERE SRC_TBL ILIKE '%{table}'
        """
        session.sql(v_sql).collect()
    st.text("Updated Successfully")
            

if "database" not in st.session_state:
    st.session_state["database"] = []
    fetch_database()

if "schemas" not in st.session_state:
    st.session_state["schemas"] = []

if "tables" not in st.session_state:
    st.session_state["tables"] = []
    

try:
    with st.sidebar:
        st.title("YAML GENERATOR")
        schema = ""
        table = ""
        
        db = st.selectbox("Select Database", st.session_state["database"], index = None,key = "db_key")

       
    
        if db != "" and db != None and db != st.session_state["db"]:
            fetch_schema(db)
            st.session_state["db"] = db
        if len(st.session_state["schemas"]) > 0:
            schema = st.selectbox("Select Schema", st.session_state["schemas"], index = None, key = "key_schema")
        if schema != "" and schema != None and schema != st.session_state["schema"]:
            fetch_table(db, schema)
            st.session_state["schema"] = schema
        if len(st.session_state["tables"]) > 0:
            table = st.multiselect("Select Table/View", st.session_state["tables"], key = "key_table")
    
        if table != "" and table != None and table != [] :
            st.session_state.table = table
            st.button("Generate YAML", key="yam_but", on_click=build_metadata, args=(st.session_state["db"], st.session_state["schema"], st.session_state.table))
            #a = st.button("Generate YAML", key="yam_but")

            #build_metadata(st.session_state["db"], st.session_state["schema"], st.session_state.table)
            
            #build_metadata(db, schema, table)
    if st.session_state.yaml_tbl != {}:
        file_name = st.session_state.table[-1]
        output = yaml.dump(st.session_state.yaml_tbl, sort_keys=False)
        with st.session_state.main_window:
            if output != "" and output != None:
                row = st.columns(4)
                if len(st.session_state.table) == 1:
                    row[1].button("Update YAML in Streamlit Metadata", key="update_meta", on_click=update_streamlit, args=(output, file_name), disabled = st.session_state["disabled"])
                row[2].download_button("Download YAML",output ,fr"{file_name}.yml", "text/yaml", key='download-yaml')
                st.code(output, language="yaml")
    
except Exception as e:
    with st.session_state.main_window:
        qry_msg = " Below is the Query Failed" if st.session_state["sql"] != "" else ""
        st.error(str(e) + qry_msg)
        if st.session_state["sql"] != "":
            st.code(st.session_state["sql"], "sql")
        
        



with bottom:
    st.title("DTCC")

css = f"""
div[data-testid="stSidebarContent"] {{
background-color: {st.session_state["green_color"]};
color:{st.session_state["white_color"]}; 
}}

div[data-testid="stSidebarContent"] h1  {{
background-color: {st.session_state["green_color"]};
color:{st.session_state["white_color"]}; 
}}

div.stMainBlockContainer {{
background-color: {st.session_state["white_color"]};
}}

div.stMainBlockContainer p {{
color: {st.session_state["green_color"]};
}}

div.st-key-bottom h1 {{
background-color:{st.session_state["green_color"]}; 
color:{st.session_state["white_color"]}; 
text-align: right;
font-family: "Lustra Black", "sans-serif";
}}

button[kind="secondary"] {{
background-color: {st.session_state["orange_color"]};
color: {st.session_state["white_color"]};
}}

button[kind="secondary"] p{{
background-color: {st.session_state["orange_color"]};
color: {st.session_state["white_color"]};
}}
"""

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)