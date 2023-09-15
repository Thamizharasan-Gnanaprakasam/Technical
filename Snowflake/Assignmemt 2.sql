CREATE OR REPLACE DATABASE EXERCISE_DB
WITH
COMMENT = "ASSIGNMENT 2";

USE DATABASE EXERCISE_DB;

USE SCHEMA PUBLIC;

CREATE OR REPLACE TABLE CUSTOMERS
(ID INT,
first_name varchar,
last_name varchar,
email varchar,
age int,
city varchar);

COPY INTO CUSTOMERS
FROM s3://snowflake-assignments-mc/gettingstarted/customers.csv
FILE_FORMAT = (TYPE="CSV", 
			   SKIP_HEADER = 1, 
			   FIELD_DELIMITER = ',');

SELECT COUNT(1) FROM CUSTOMERS;