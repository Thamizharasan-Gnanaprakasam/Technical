SHOW TABLES IN DATABASE OUR_FIRST_DB;

SELECT * FROM OUR_FIRST_DB.PUBLIC.EMPLOYEES; -- 200
SELECT * FROM OUR_FIRST_DB.PUBLIC.EMPLOYEES1; -- 0

ALTER TABLE OUR_FIRST_DB.PUBLIC.EMPLOYEES
SWAP WITH OUR_FIRST_DB.PUBLIC.EMPLOYEES1;

SELECT * FROM OUR_FIRST_DB.PUBLIC.EMPLOYEES; -- 0
SELECT * FROM OUR_FIRST_DB.PUBLIC.EMPLOYEES1; -- 200

SHOW SCHEMAS IN DATABASE OUR_FIRST_DB;

CREATE OR REPLACE TRANSIENT SCHEMA COPY_DB.SECOND_SCHEMA;

SHOW TABLES IN SCHEMA COPY_DB.PUBLIC; --4
SHOW TABLES IN SCHEMA COPY_DB.SECOND_SCHEMA; --0

ALTER SCHEMA COPY_DB.PUBLIC
SWAP WITH COPY_DB.SECOND_SCHEMA;

SHOW TABLES IN SCHEMA COPY_DB.PUBLIC; --0
SHOW TABLES IN SCHEMA COPY_DB.SECOND_SCHEMA; --4