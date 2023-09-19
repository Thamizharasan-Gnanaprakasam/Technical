CREATE OR REPLACE TABLE employees
(
customer_id int,
first_name varchar(50),
last_name varchar(50),
email varchar(50),
age int,
department varchar(50)
);

CREATE OR REPLACE STAGE AWS_ASSIGN5_STAGE
URL =  's3://snowflake-assignments-mc/copyoptions/example1/';

ls @AWS_ASSIGN5_STAGE;

CREATE OR REPLACE FILE FORMAT ASSIGN5_FF
WITH
TYPE = CSV,
FIELD_DELIMITER = ',',
SKIP_HEADER = 1;



DESC FILE FORMAT ASSIGN5_FF;

COPY INTO EMPLOYEES
FROM @AWS_ASSIGN5_STAGE
FILE_FORMAT = (FORMAT_NAME = ASSIGN5_FF)
FILES = ('employees.csv')
VALIDATION_MODE = RETURN_ERRORS; -- Line# 10, Character - 1, Error: Numeric value '-' is not recognized

COPY INTO EMPLOYEES
FROM @AWS_ASSIGN5_STAGE
FILE_FORMAT = (FORMAT_NAME = ASSIGN5_FF)
FILES = ('employees.csv')
VALIDATION_MODE = RETURN_1_ROWS; -- This as well return error even though line# 10 has invalid data

COPY INTO EMPLOYEES
FROM @AWS_ASSIGN5_STAGE
FILE_FORMAT = (FORMAT_NAME = ASSIGN5_FF)
FILES = ('employees.csv')
ON_ERROR = CONTINUE; -- ROWS PARSED - 122, LOADED - 121
