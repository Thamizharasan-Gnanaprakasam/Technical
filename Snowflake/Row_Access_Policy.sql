USE DATABASE DATA_S;

USE SCHEMA PUBLIC;

CREATE OR REPLACE ROLE HOME_MANAGER;

SHOW GRANTS ON ROLE HOME_MANAGER;
SHOW GRANTS OF ROLE HOME_MANAGER;

GRANT ROLE HOME_MANAGER TO USER TAMIL;

SELECT * FROM ORDERS;

CREATE OR REPLACE ROW ACCESS POLICY CATEGORY_POLICY AS
(CATEGORY VARCHAR) RETURNS BOOLEAN ->
CASE WHEN CURRENT_ROLE() = 'HOME_MANAGER' AND CATEGORY = 'Furniture' THEN TRUE
WHEN CURRENT_ROLE() = 'ACCOUNTADMIN' THEN TRUE
ELSE FALSE END;

ALTER TABLE ORDERS
ADD ROW ACCESS POLICY CATEGORY_POLICY ON (CATEGORY);

USE ROLE HOME_MANAGER;
SELECT * FROM ORDERS;

USE ROLE ACCOUNTADMIN;

GRANT USAGE ON DATABASE DATA_S TO ROLE HOME_MANAGER;
GRANT USAGE ON SCHEMA DATA_S.PUBLIC TO ROLE HOME_MANAGER;
GRANT SELECT ON TABLE ORDERS TO ROLE HOME_MANAGER;
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE HOME_MANAGER;


USE ROLE ACCOUNTADMIN;
SELECT * FROM ORDERS;

USE ROLE ANALYST_FULL;
SELECT * FROM ORDERS;

TO DROP ROW POLICY -- DROP ROW ACCESS POLICY POLICY_NAME
TO DROP ALL ROW POLICY -- DROP ROW ACCESS POLICIES

USE ROLE ACCOUNTADMIN;

GRANT USAGE ON DATABASE DATA_S TO ROLE ANALYST_FULL;
GRANT USAGE ON SCHEMA DATA_S.PUBLIC TO ROLE ANALYST_FULL;
GRANT SELECT ON TABLE ORDERS TO ROLE ANALYST_FULL;
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE ANALYST_FULL;