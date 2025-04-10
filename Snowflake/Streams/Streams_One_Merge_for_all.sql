SELECT * FROM SALES_RAW_STAGING;

SELECT * FROM SALES_STREAM;

--DELETE PAPAYA
--UPDATE APPLE TO PINEAPPLE
--INSERT ORANGE

DELETE FROM SALES_RAW_STAGING WHERE PRODUCT='Papaya';

UPDATE SALES_RAW_STAGING SET PRODUCT = 'Pineapple' WHERE PRODUCT = 'Apple';

INSERT INTO SALES_RAW_STAGING VALUES
(8,'Orange',2.99,2,1);

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
