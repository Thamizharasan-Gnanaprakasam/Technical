CREATE OR REPLACE STAGE MANAGE_DB.EXTERNAL_STAGES.AWS_STAGE_ERROREX
URL = 's3://bucketsnowflakes4';

list @MANAGE_DB.EXTERNAL_STAGES.AWS_STAGE_ERROREX; -- File OrderDetails_error.csv has invalid data

CREATE OR REPLACE TABLE OUR_FIRST_DB.PUBLIC.ORDERS(
ORDERID VARCHAR(30),
AMOUNT INT,
PROFIT INT,
QUANTITY INT,
CATEGORY VARCHAR(30),
SUBCATEGORY VARCHAR(30)
);

--DEFAULT COPY STATEMENT
COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS
FROM @MANAGE_DB.EXTERNAL_STAGES.AWS_STAGE_ERROREX
FILE_FORMAT = (TYPE='CSV', FIELD_DELIMITER = ',' , SKIP_HEADER = 1)
FILES = ('OrderDetails_error.csv', 'OrderDetails_error2.csv'); -- This will fail has there is an invalid data in file 1

SELECT * FROM OUR_FIRST_DB.PUBLIC.ORDERS;

--COPY STATEMENT - WITH ON_ERROR = CONTINUE - THIS WILL SKIP THE ROWS WHICH HAS INVALID DATA AND CONTINUE LOADING OTEHR ROWS
COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS
FROM @MANAGE_DB.EXTERNAL_STAGES.AWS_STAGE_ERROREX
FILE_FORMAT = (TYPE='CSV', FIELD_DELIMITER = ',' , SKIP_HEADER = 1)
ON_ERROR = 'CONTINUE'
FILES = ('OrderDetails_error.csv', 'OrderDetails_error2.csv'); -- This will be Partial load success (ignore the rows which has invalid data)

--COPY STATEMENT - WITH ON_ERROR = ABORT_STATEMENT - DEFAULT - WILL NOT LOAD BOTH THE FILES
TRUNCATE OUR_FIRST_DB.PUBLIC.ORDERS;

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS
FROM @MANAGE_DB.EXTERNAL_STAGES.AWS_STAGE_ERROREX
FILE_FORMAT = (TYPE='CSV', FIELD_DELIMITER = ',' , SKIP_HEADER = 1)
ON_ERROR = 'ABORT_STATEMENT'
FILES = ('OrderDetails_error.csv', 'OrderDetails_error2.csv'); -- This will fail has there is an invalid data in file 1

SELECT count(1) FROM OUR_FIRST_DB.PUBLIC.ORDERS;

SELECT count(1) FROM OUR_FIRST_DB.PUBLIC.ORDERS;

--COPY STATEMENT - WITH ON_ERROR = SKIP_FILE - THIS WILL SKIP THE THE ENTIRE FILE WHICH HAS INVALID DATA (EVEN 1 ROW HAS INVALID DATA)

TRUNCATE  OUR_FIRST_DB.PUBLIC.ORDERS;

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS
FROM @MANAGE_DB.EXTERNAL_STAGES.AWS_STAGE_ERROREX
FILE_FORMAT = (TYPE='CSV', FIELD_DELIMITER = ',' , SKIP_HEADER = 1)
ON_ERROR = 'SKIP_FILE'
FILES = ('OrderDetails_error.csv', 'OrderDetails_error2.csv'); -- Only file 2 will be loaded

SELECT count(1) FROM OUR_FIRST_DB.PUBLIC.ORDERS;

--COPY STATEMENT - WITH ON_ERROR = SKIP_FILE_<number> - THIS WILL SKIP THE THE ENTIRE FILE IF THE <number> (ERROR_LIMIT) SPECIFIED IN SKIP_FILE IS LESSER OR EQUAL TO ERROR_SEEN  

TRUNCATE  OUR_FIRST_DB.PUBLIC.ORDERS;

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS
FROM @MANAGE_DB.EXTERNAL_STAGES.AWS_STAGE_ERROREX
FILE_FORMAT = (TYPE='CSV', FIELD_DELIMITER = ',' , SKIP_HEADER = 1)
ON_ERROR = 'SKIP_FILE_3'
FILES = ('OrderDetails_error.csv', 'OrderDetails_error2.csv'); -- This is same as Continue as the error limit is 3 and error_seen is 2

SELECT count(1) FROM OUR_FIRST_DB.PUBLIC.ORDERS;

TRUNCATE  OUR_FIRST_DB.PUBLIC.ORDERS;

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS
FROM @MANAGE_DB.EXTERNAL_STAGES.AWS_STAGE_ERROREX
FILE_FORMAT = (TYPE='CSV', FIELD_DELIMITER = ',' , SKIP_HEADER = 1)
ON_ERROR = 'SKIP_FILE_2'
FILES = ('OrderDetails_error.csv', 'OrderDetails_error2.csv'); -- This will not load the file 1 as the error_limit (2) and error_seen (2) are equal

SELECT count(1) FROM OUR_FIRST_DB.PUBLIC.ORDERS;

--COPY STATEMENT - WITH ON_ERROR = SKIP_FILE_<percent> - THIS WILL SKIP THE THE ENTIRE FILE IF ERROR_SEEN COUNT IS GREATED THAN THE ERROR_LIMIT GIVE IN <percent>

TRUNCATE  OUR_FIRST_DB.PUBLIC.ORDERS;

COPY INTO OUR_FIRST_DB.PUBLIC.ORDERS
FROM @MANAGE_DB.EXTERNAL_STAGES.AWS_STAGE_ERROREX
FILE_FORMAT = (TYPE='CSV', FIELD_DELIMITER = ',' , SKIP_HEADER = 1)
ON_ERROR = 'SKIP_FILE_3%'
FILES = ('OrderDetails_error.csv', 'OrderDetails_error2.csv'); -- This will skip only the 2 rows in file 1 as the error limit is set to 3% which is 45 rows

SELECT count(1) FROM OUR_FIRST_DB.PUBLIC.ORDERS;
