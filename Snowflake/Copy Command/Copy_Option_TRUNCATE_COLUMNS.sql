/*TRUNCATECOLUMNS = TRUE | FALSE
THIS IS TO SPECIFY TO TRUNCATE THE TEXT STRING THAT EXCEED THE SIZE OF TARGET COLUMN*/ 

CREATE OR REPLACE TABLE COPY_DB.PUBLIC.ORDERS (
ORDER_ID VARCHAR(30),
AMOUNT VARCHAR(30),
PROFIT INT,
QUANTITY INT,
CATEGORY VARCHAR(10),
SUBCATEGORY VARCHAR(30)
);

CREATE OR REPLACE STAGE COPY_DB.PUBLIC.AWS_STAGE_COPY
URL = 's3://snowflakebucket-copyoption/size/';


COPY INTO ORDERS
FROM @COPY_DB.PUBLIC.AWS_STAGE_COPY
FILE_FORMAT = (TYPE = CSV, FIELD_DELIMITER = ',', SKIP_HEADER = 1)
PATTERN = '.*Order.*'; -- THIS WILL NOT WORK, AS THE SIZE OF CATEGORY VALUE IN FILE IS MORE THAN 10 (SIZE DEFINED IN TABLE)

COPY INTO ORDERS
FROM @COPY_DB.PUBLIC.AWS_STAGE_COPY
FILE_FORMAT = (TYPE = CSV, FIELD_DELIMITER = ',', SKIP_HEADER = 1)
PATTERN = '.*Order.*'
TRUNCATECOLUMNS = TRUE; -- THIS WILL WORK, THIS WILL TRUNCATE THE VALUES OF CATEGORY IN FILE TO 10 CHARACTERS AND LOAD INTO TABLE