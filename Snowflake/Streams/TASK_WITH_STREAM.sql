CREATE OR REPLACE TASK SALES_TASK
WAREHOUSE = COMPUTE_WH
SCHEDULE ='1 MINUTE'
WHEN SYSTEM$STREAM_HAS_DATA('SALES_STREAM')
AS
MERGE INTO SALES_FINAL_TABLE A
USING (SELECT A.ID,
A.PRODUCT,
A.PRICE,
A.AMOUNT,
A.METADATA$ACTION,
A.METADATA$ISUPDATE,
B.STORE_ID,
B.LOCATION,
B.EMPLOYEES
FROM
SALES_STREAM A
INNER JOIN STORE_TABLE B
ON A.STORE_ID = B.STORE_ID) B
ON A.ID = B.ID
WHEN MATCHED
    AND B.METADATA$ACTION = 'DELETE'
    AND B.METADATA$ISUPDATE = FALSE
    THEN DELETE
WHEN MATCHED
    AND B.METADATA$ACTION = 'INSERT'
    AND B.METADATA$ISUPDATE = TRUE
    THEN UPDATE
    SET A.ID = B.ID,
    A.PRODUCT = B.PRODUCT,
    A.PRICE = B.PRICE,
    A.AMOUNT = B.AMOUNT
WHEN NOT MATCHED
    AND B.METADATA$ACTION = 'INSERT'
    AND B.METADATA$ISUPDATE = FALSE
    THEN
    INSERT 
    (ID, PRODUCT, PRICE,AMOUNT,STORE_ID,LOCATION,EMPLOYEES)
    VALUES
    (B.ID,B.PRODUCT,B.PRICE,B.AMOUNT,B.STORE_ID,B.LOCATION,B.EMPLOYEES);

ALTER TASK SALES_TASK RESUME;

DELETE FROM SALES_RAW_STAGING WHERE PRODUCT='Orange';

UPDATE SALES_RAW_STAGING SET PRODUCT = 'Apple' WHERE PRODUCT = 'Pineapple';    

INSERT INTO SALES_RAW_STAGING VALUES
(8,'Grapes',2.99,2,1);

select * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(TASK_NAME => 'SALES_TASK'));

SHOW STREAMS;
    