CREATE OR REPLACE STAGE ASSIGN7_STAGE
URL =  's3://snowflake-assignments-mc/unstructureddata/';

LS @ASSIGN7_STAGE;

CREATE OR REPLACE FILE FORMAT FILE_FORMATS.ASSIGN7_FF
TYPE = JSON;

CREATE OR REPLACE TABLE PUBLIC.JSON_RAW
(
RAW VARIANT
);

COPY INTO PUBLIC.JSON_RAW
FROM @ASSIGN7_STAGE
FILE_FORMAT = (FORMAT_NAME = FILE_FORMATS.ASSIGN7_FF)
FILES = ('Jobskills.json');

SELECT * FROM PUBLIC.JSON_RAW;