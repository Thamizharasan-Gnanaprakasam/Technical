/*
Normal View will take more time for each execution of a query

To avoid this, we can use materialized view, which will create a table using the select statement and update the table frequency by the update service provided by SF

with this, we can have speed for table query execution and also get the realtime data

WHEN TO USE MATERIALIZED VIEW:
    > When normal view is used frequently and takng long time
    > If the data is not updated frequently in the base table

Considerations to use MV:
    > Data should not update frequently
    > Maintance cost

Alternatives for MV
    > We can use Streams and Task instead of MV if the data is keep on updating/inserting in the base table

Limitaions
    > MV is available only from Enterpise Edition and higher
    > Joins is not possible in MV (including self-join)
    > Only Limited aggregation functins can be used
    > No Having Clause
    > No Order by Clause
    > No UDFs
    > No Limit Clause

*/


SHOW PARAMETERS;

ALTER SESSION SET USE_CACHED_RESULT = FALSE;
ALTER WAREHOUSE COMPUTE_WH SUSPEND;
ALTER WAREHOUSE COMPUTE_WH RESUME;

CREATE OR REPLACE TRANSIENT DATABASE ORDERS;

CREATE OR REPLACE SCHEMA TPCH_SF100;

CREATE OR REPLACE TABLE TPCH_SF100.ORDERS  AS
SELECT * FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF100.ORDERS;

SELECT
YEAR(O_ORDERDATE) AS YEAR,
MAX(O_COMMENT) AS MAX_COMMENT,
MIN(O_COMMENT) AS MIN_COMMNET,
MAX(O_CLERK) AS MAX_CLERK,
MIN(O_CLERK) AS MIN_CLERK
FROM TPCH_SF100.ORDERS
GROUP BY 1
ORDER BY 1;

CREATE OR REPLACE MATERIALIZED VIEW ORDER_MV AS
SELECT
YEAR(O_ORDERDATE) AS YEAR,
MAX(O_COMMENT) AS MAX_COMMENT,
MIN(O_COMMENT) AS MIN_COMMNET,
MAX(O_CLERK) AS MAX_CLERK,
MIN(O_CLERK) AS MIN_CLERK
FROM TPCH_SF100.ORDERS
GROUP BY 1;


SELECT * FROM ORDER_MV
ORDER BY 1;

UPDATE ORDERS
SET O_CLERK ='TAMIL'
WHERE O_ORDERDATE='1992-01-01';

SHOW VIEWS;

--CHECK THE CREDITS OF MATERIALIZED VIEW
SELECT * FROM TABLE(ORDERS.INFORMATION_SCHEMA.MATERIALIZED_VIEW_REFRESH_HISTORY());

SHOW FUNCTIONS IN INFORMATION_SCHEMA ;