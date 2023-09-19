-- 1. Validation Mode = RETURN_n_ROWS | RETURN_ERRORS

-- With Validation Mode, no data will be loaded into table, rather it will return the data bsed on above 2 options
-- RETURN_n_ROWS - Return first n Rows from the file, if no error occured else will return the first error encountered
-- RETURN_ERRORS - Validate the file, and return all the error messages from each row

CREATE OR REPLACE DATABASE COPY_DB;

USE DATABASE COPY_DB;

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

LS @COPY_DB.PUBLIC.AWS_STAGE_COPY;

/*Print all errors*/

COPY INTO COPY_DB.PUBLIC.ORDERS
FROM @COPY_DB.PUBLIC.AWS_STAGE_COPY
PATTERN = '.*Order.*'
FILE_FORMAT = (TYPE = CSV, FIELD_DELIMITER = ',', SKIP_HEADER = 1)
--ON_ERROR = CONTINUE | ABORT | SKIP_FILE | SKIP_FILE_4 | SKIP_FILE_5%
VALIDATION_MODE = RETURN_ERRORS; -- This will not load any data to table and also no rewos will be returned as all the records a valid

SELECT COUNT(1) FROM COPY_DB.PUBLIC.ORDERS;


/*Print First n rows if no error occured*/

COPY INTO COPY_DB.PUBLIC.ORDERS
FROM @COPY_DB.PUBLIC.AWS_STAGE_COPY
PATTERN = '.*Order.*'
FILE_FORMAT = (TYPE = CSV, FIELD_DELIMITER = ',', SKIP_HEADER = 1)
--ON_ERROR = CONTINUE | ABORT | SKIP_FILE | SKIP_FILE_4 | SKIP_FILE_5%
VALIDATION_MODE = RETURN_5_ROWS; -- This will not load any data to the table and also return first 5 rows as there is no error in first 5 rows

SELECT COUNT(1) FROM COPY_DB.PUBLIC.ORDERS;


CREATE OR REPLACE STAGE COPY_DB.PUBLIC.AWS_STAGE_COPY
URL = 's3://snowflakebucket-copyoption/returnfailed/';

ls @COPY_DB.PUBLIC.AWS_STAGE_COPY;

/*Print all errors*/

COPY INTO COPY_DB.PUBLIC.ORDERS
FROM @COPY_DB.PUBLIC.AWS_STAGE_COPY
PATTERN = '.*Order.*'
FILE_FORMAT = (TYPE = CSV, FIELD_DELIMITER = ',', SKIP_HEADER = 1)
--ON_ERROR = CONTINUE | ABORT | SKIP_FILE | SKIP_FILE_4 | SKIP_FILE_5%
VALIDATION_MODE = RETURN_ERRORS; -- This will not load any data to table and also return the rows which are not valid with the error description

SELECT COUNT(1) FROM COPY_DB.PUBLIC.ORDERS;


/*Print First n rows if no error occured*/

COPY INTO COPY_DB.PUBLIC.ORDERS
FROM @COPY_DB.PUBLIC.AWS_STAGE_COPY
PATTERN = '.*error.*'
FILE_FORMAT = (TYPE = CSV, FIELD_DELIMITER = ',', SKIP_HEADER = 1)
--ON_ERROR = CONTINUE | ABORT | SKIP_FILE | SKIP_FILE_4 | SKIP_FILE_5%
VALIDATION_MODE = RETURN_5_ROWS; -- This will not load any data to the table and throws the error message of first error encountered in the file