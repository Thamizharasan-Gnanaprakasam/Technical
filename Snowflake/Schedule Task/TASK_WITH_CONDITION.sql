CREATE OR REPLACE TASK CUSTOMERS3_TASK1
WAREHOUSE = COMPUTE_WH
SCHEDULE = '1 MINUTE'
WHEN 1=2
AS
INSERT INTO CUSTOMERS3 (NAME) VALUES ('NO INSERT');

CREATE OR REPLACE TASK CUSTOMERS3_TASK2
WAREHOUSE = COMPUTE_WH
SCHEDULE = '1 MINUTE'
WHEN 1=1
AS
INSERT INTO CUSTOMERS3 (NAME) VALUES ('INSERT');

ALTER TASK CUSTOMERS3_TASK1 RESUME;
ALTER TASK CUSTOMERS3_TASK2 RESUME;

SELECT * FROM CUSTOMERS3;

SELECT * FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY())
WHERE NAME IN ('CUSTOMERS3_TASK1','CUSTOMERS3_TASK2');

ALTER TASK CUSTOMERS3_TASK1 SUSPEND;
ALTER TASK CUSTOMERS3_TASK2 SUSPEND;

--ONLY FUNCTION WE CAN USE IN TASK CONDITION - SYSTEM$STREAM_HAS_DATA('<STREAM_NAME>')

CREATE OR REPLACE TASK CUSTOMERS3_TASK2
WAREHOUSE = COMPUTE_WH
SCHEDULE = '1 MINUTE'
WHEN SYSTEM$STREAM_HAS_DATA('<STREAM_NAME>')
AS
INSERT INTO CUSTOMERS3 (NAME) VALUES ('INSERT');