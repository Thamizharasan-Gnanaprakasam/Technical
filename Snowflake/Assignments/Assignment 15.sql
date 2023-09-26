USE DEMO_DB;
USE ROLE ACCOUNTADMIN;

-- Prepare table --
create or replace table customers(
  id number,
  full_name varchar, 
  email varchar,
  phone varchar,
  spent number,
  create_date DATE DEFAULT CURRENT_DATE);
 
 
-- insert values in table --
insert into customers (id, full_name, email,phone,spent)
values
  (1,'Lewiss MacDwyer','lmacdwyer0@un.org','262-665-9168',140),
  (2,'Ty Pettingall','tpettingall1@mayoclinic.com','734-987-7120',254),
  (3,'Marlee Spadazzi','mspadazzi2@txnews.com','867-946-3659',120),
  (4,'Heywood Tearney','htearney3@patch.com','563-853-8192',1230),
  (5,'Odilia Seti','oseti4@globo.com','730-451-8637',143),
  (6,'Meggie Washtell','mwashtell5@rediff.com','568-896-6138',600);


  -- set up roles
CREATE OR REPLACE ROLE ANALYST_MASKED;
CREATE OR REPLACE ROLE ANALYST_FULL;
 
-- grant select on table to roles
GRANT SELECT ON TABLE DEMO_DB.PUBLIC.CUSTOMERS TO ROLE ANALYST_MASKED;
GRANT SELECT ON TABLE DEMO_DB.PUBLIC.CUSTOMERS TO ROLE ANALYST_FULL;
 
GRANT USAGE ON SCHEMA DEMO_DB.PUBLIC TO ROLE ANALYST_MASKED;
GRANT USAGE ON SCHEMA DEMO_DB.PUBLIC TO ROLE ANALYST_FULL;
 
-- grant warehouse access to roles
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE ANALYST_MASKED;
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE ANALYST_FULL;
 
-- assign roles to a user
GRANT ROLE ANALYST_MASKED TO USER TAMIL;
GRANT ROLE ANALYST_FULL TO USER TAMIL;

SHOW MASKING POLICIES;

SELECT * FROM TABLE(INFORMATION_SCHEMA.POLICY_REFERENCES(POLICY_NAME => 'NAME'));

CREATE OR REPLACE MASKING POLICY NAME AS
(VAL VARCHAR) RETURNS VARCHAR ->
CASE WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN','ANALYST_FULL') THEN VAL
ELSE '***' END;

ALTER TABLE CUSTOMERS MODIFY COLUMN FULL_NAME
SET MASKING POLICY NAME;

USE ROLE ANALYST_FULL;
SELECT * FROM CUSTOMERS;

USE ROLE ANALYST_MASKED;
SELECT * FROM CUSTOMERS;

USE ROLE ACCOUNTADMIN;

ALTER MASKING POLICY NAME SET BODY ->
CASE WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN','ANALYST_FULL') THEN VAL
ELSE '***' || RIGHT(VAL,2) END;

USE ROLE ANALYST_FULL;
SELECT * FROM CUSTOMERS;

USE ROLE ANALYST_MASKED;
SELECT * FROM CUSTOMERS;