/* SIZE LIMIT - Specify the max size (in bytes) of data loaded in copy command (atleast one file) 
When threshold is exceed, copy command will stop loading*/

CREATE OR REPLACE TABLE COPY_DB.PUBLIC.ORDERS (
ORDER_ID VARCHAR(30),
AMOUNT VARCHAR(30),
PROFIT INT,
QUANTITY INT,
CATEGORY VARCHAR(30),
SUBCATEGORY VARCHAR(30)
);

CREATE OR REPLACE STAGE COPY_DB.PUBLIC.AWS_STAGE_COPY
URL = 's3://snowflakebucket-copyoption/size/';

ls @COPY_DB.PUBLIC.AWS_STAGE_COPY;

COPY INTO ORDERS
FROM @COPY_DB.PUBLIC.AWS_STAGE_COPY
FILE_FORMAT = (TYPE = CSV, FIELD_DELIMITER=',', SKIP_HEADER=1)
SIZE_LIMIT = 20000; -- This will load only one file as the size of first fileitself exceed the treshold limit

CREATE OR REPLACE TABLE COPY_DB.PUBLIC.ORDERS (
ORDER_ID VARCHAR(30),
AMOUNT VARCHAR(30),
PROFIT INT,
QUANTITY INT,
CATEGORY VARCHAR(30),
SUBCATEGORY VARCHAR(30)
);

COPY INTO ORDERS
FROM @COPY_DB.PUBLIC.AWS_STAGE_COPY
FILE_FORMAT = (TYPE = CSV, FIELD_DELIMITER=',', SKIP_HEADER=1)
SIZE_LIMIT = 60000; -- This will load both the files as the size of first file is not exceed the size_limit