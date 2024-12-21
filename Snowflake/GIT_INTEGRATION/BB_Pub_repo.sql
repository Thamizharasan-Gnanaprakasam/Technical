CREATE OR REPLACE API INTEGRATION my_bb_pub_api
API_PROVIDER = GIT_HTTPS_API
API_ALLOWED_PREFIXES = ('https://bitbucket.org/thamizharasangnanaprakasam')
ENABLED = TRUE;

--git clone https://thamizharasangnanaprakas-admin@bitbucket.org/thamizharasangnanaprakasam/my_public_repo.git

CREATE OR REPLACE GIT REPOSITORY my_bb_pub_repo
API_INTEGRATION = my_bb_pub_api
ORIGIN = 'https://bitbucket.org/thamizharasangnanaprakasam/my_public_repo';

SHOW GIT BRANCHES IN GIT REPOSITORY my_bb_pub_repo;

alter git repository my_bb_pub_repo fetch;

LS @my_bb_pub_repo/branches/main;

CREATE OR REPLACE TABLE EMPLOYEE
(
ID INTEGER,
COL1 VARCHAR,
COL2 VARCHAR
);

INSERT INTO EMPLOYEE
VALUES
(1, 'TEST','TEST1'),
(2, 'TEST','TEST2'),
(3, 'TEST','TEST3'),
(4, 'TEST','TEST4'),
(5, 'TEST','TEST5');

select current_account();

CREATE OR REPLACE PROCEDURE FILTER_TABLE(TABLE_NAME STRING, COL_NAME STRING) 
 RETURNS TABLE(ID INTEGER, COL1 VARCHAR, COL2 VARCHAR)
LANGUAGE  PYTHON
RUNTIME_VERSION = 3.8
PACKAGES = ('snowflake-snowpark-python')
IMPORTS = ('@my_bb_pub_repo/branches/main/filter.py')
HANDLER = 'filter.filter_col';

CALL FILTER_TABLE('BITBUCKET.PUBLIC.EMPLOYEE','ID');