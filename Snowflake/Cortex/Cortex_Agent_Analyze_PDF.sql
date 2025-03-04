CREATE OR REPLACE DATABASE PDF_DB;
CREATE OR REPLACE SCHEMA PDF_SCHEMA;
CREATE OR REPLACE STAGE PDF_STAGE
DIRECTORY = (ENABLE= TRUE);

call SYSTEM$PIP_INSTALL('textract');


CREATE OR REPLACE FUNCTION PDF_CHUNKS(FILE_URL VARCHAR)
RETURNS TABLE(CHUNKS VARCHAR)
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
HANDLER = 'ProcessPDF'
PACKAGES = ('langchain', 'pandas', 'snowflake-snowpark-python', 'PyPDF2', 'PyCryptodome')
AS
$$
from langchain.text_splitter import RecursiveCharacterTextSplitter
from snowflake.snowpark.files import SnowflakeFile
import pandas as pd
import io
import PyPDF2

class ProcessPDF:
    def read_pdf(self, file_url: str):
        pass
        with SnowflakeFile.open(file_url, 'rb') as f:
            buffer_data = io.BytesIO(f.read())

        reader = PyPDF2.PdfReader(buffer_data)
        text = ""
        for page in reader.pages:
            text += page.extract_text().replace("\n"," ").replace("\0"," ")

        return text

    def process(self, file_url: str):
        data = self.read_pdf(file_url)
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap = 300,
        length_function = len
        )
        chunks = text_splitter.split_text(data)
        df = pd.DataFrame(chunks, columns = ["chunks"])
        yield from df.itertuples(index= False, name=None)
    
$$;

CREATE OR REPLACE TABLE PDF_TBL AS
SELECT
RELATIVE_PATH,
BUILD_SCOPED_FILE_URL(@PDF_STAGE, RELATIVE_PATH) FILE_URL,
CONCAT(RELATIVE_PATH,': ', B.CHUNKS) AS CHUNKS,
'English' as Language
FROM DIRECTORY(@PDF_STAGE), table(PDF_CHUNKS(BUILD_SCOPED_FILE_URL(@PDF_STAGE, RELATIVE_PATH))) B;

select * from DIRECTORY(@PDF_STAGE), table(PDF_CHUNKS(BUILD_SCOPED_FILE_URL(@PDF_STAGE, RELATIVE_PATH))) B;

SELECT * FROM PDF_TBL;


CREATE OR REPLACE CORTEX SEARCH SERVICE PDF_SUMMARIZE
ON CHUNKS
ATTRIBUTES RELATIVE_PATH, FILE_URL, LANGUAGE
WAREHOUSE = COMPUTE_WH
TARGET_LAG = '1 HOUR'
AS
(
SELECT
*
FROM PDF_TBL
);


SHOW CORTEX SEARCH SERVICES;

SELECT PDF_SUMMARIZE("SUMMARIZE PDF",["CHUNKS"]);

DESC CORTEX SEARCH SERVICE PDF_SUMMARIZE;