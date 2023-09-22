/*Snow Pipe will load data autoamtically if the file is available in S3
This uses serverless feature instead of Virtaul WH
Wih snowpipe, the data will be available in relatime for analysis
Snowpipe will trigger within 30 to 60 Secs after the file is placed in S3*/

CREATE OR REPLACE TABLE OUR_FIRST_DB.PUBLIC.EMPLOYEES (
ID INT,
FIRST_NAME STRING,
LAST_NAME STRING,
EMAIL STRING,
LOCATION STRING,
DEPARTMENT STRING
);


//FILE FORMAT
DESC FILE FORMAT MANAGE_DB.FILE_FORMATS.CSV_FILEFORMAT;

//STAGE
DESC STAGE MANAGE_DB.EXTERNAL_STAGES.S3_STAGE_CSV;

CREATE OR REPLACE STAGE MANAGE_DB.EXTERNAL_STAGES.S3_STAGE_CSV
URL = 's3://snowflakes3buckettamil123/csv/snowflake',
STORAGE_INTEGRATION = S3_INT,
FILE_FORMAT = MANAGE_DB.FILE_FORMATS.CSV_FILEFORMAT;

//SCHEMA FOR PIPES
CREATE OR REPLACE SCHEMA MANAGE_DB.PIPES_SCHEMA;

//PIPE CREATION
CREATE OR REPLACE PIPE MANAGE_DB.PIPES_SCHEMA.S3_PIPE
AUTO_INGEST = TRUE
AS
COPY INTO OUR_FIRST_DB.PUBLIC.EMPLOYEES
FROM @MANAGE_DB.EXTERNAL_STAGES.S3_STAGE_CSV;

//DESC PIPE
DESC PIPE MANAGE_DB.PIPES_SCHEMA.S3_PIPE;
--arn:aws:sqs:us-east-1:959845688343:sf-snowpipe-AIDA5662C4QLWINJHEIGF-3iFoZ-hZZsJdBqssppgeZA

SHOW PIPES;

//refreseh pipe
ALTER PIPE MANAGE_DB.PIPES_SCHEMA.S3_PIPE REFRESH; -- THIS WILL INTMATE ANY NEW FILE SENT TO PIPE

//CHECK STATUS OF PIPE
SELECT SYSTEM$PIPE_STATUS('MANAGE_DB.PIPES_SCHEMA.S3_PIPE');

//SNOWPIPE ERROR MESSAGE - THIS WILL NOT GIVE EXACT ERROR MESSAGE
SELECT * FROM TABLE(VALIDATE_PIPE_LOAD(PIPE_NAME => 'MANAGE_DB.PIPES_SCHEMA.S3_PIPE',
                                        START_TIME => DATEADD('HOURS',-2,CURRENT_TIMESTAMP())));

//ANOTHER WAY TO GET ERROR MESSAGE
SELECT * FROM TABLE(MANAGE_DB.INFORMATION_SCHEMA.COPY_HISTORY(TABLE_NAME => 'OUR_FIRST_DB.PUBLIC.EMPLOYEES2',
                                                            START_TIME => DATEADD('HOURS',-2,CURRENT_TIMESTAMP)));