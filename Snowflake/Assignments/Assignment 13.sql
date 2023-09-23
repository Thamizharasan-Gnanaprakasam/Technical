USE DATABASE DEMO_DB;
USE SCHEMA PUBLIC;

SELECT * FROM "SNOWFLAKE_SAMPLE_DATA"."TPCDS_SF10TCL"."CUSTOMER_ADDRESS" ;

CREATE OR REPLACE TABLE CUSTOMER_ADDRESS_SAMPLE_5 AS
SELECT * FROM "SNOWFLAKE_SAMPLE_DATA"."TPCDS_SF10TCL"."CUSTOMER_ADDRESS"
SAMPLE ROW (5) SEED (2);

CREATE OR REPLACE TABLE CUSTOMER_SAMPLE_1
AS SELECT * FROM "SNOWFLAKE_SAMPLE_DATA"."TPCDS_SF10TCL"."CUSTOMER"
SAMPLE BLOCK (1) SEED (2);

SELECT COUNT(1) FROM CUSTOMER_SAMPLE_1; --535,183