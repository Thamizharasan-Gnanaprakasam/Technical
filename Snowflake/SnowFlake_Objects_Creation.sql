-- ACCOUNT: https://vgrgbai-gjb39117.snowflakecomputing.com/console/login.

-- DATABASE CREATION
-- Create a database from the share.
create database snowflake_sample_data from share sfc_samples.sample_data;

-- Grant the PUBLIC role access to the database.
-- Optionally change the role name to restrict access to a subset of users.
grant imported privileges on database snowflake_sample_data to role public;

--WAREHOUSE CREATION

/*
Size of WH:
XSMALL	-	Servers	-	1 	-	Credits	-	1/hour
SMALL	-	Servers	-	2	-	Credits	-	2/hour
MEDIUM	-	Servers	-	4	-	Credits	-	4/hour
LARGE 	-	Servers	-	8	-	Credits	-	8/hour
XLARGE 	-	Servers	-	16	-	Credits	-	16/hour
2XLARGE -	Servers -	32	-	Credits	-	32/hour
3XLARGE -	Servers	-	64	-	Credits	-	64/hour
4XLARGE -	Servers	-	128	-	Credits	-	128/hour
5XLARGE -	Servers	-	256	-	Credits	-	256/hour
6XLARGE -	Servers	-	512	-	Credits	-	512/hour

Cost
Compute: $2/credit (Standard), $3/Credit (Enterprice), $4/Credit (Business Critical), Contack SF for Virtual Private -> Differ based on region and platform
Storage: $2/TB
*/

CREATE OR REPLACE WAREHOUSE SECOND_WH
WITH
WAREHOUSE_SIZE = XSMALL
MIN_CLUSTER_COUNT = 1
MAX_CLUSTER_COUNT = 3
AUTO_SUSPEND = 600 -- IN SECONDS
AUTO_RESUME = TRUE
WAREHOUSE_TYPE = STANDARD
SCALING_POLICY=STANDARD
INITIALLY_SUSPENDED = TRUE
COMMENT = 'MY SECOND WH';

--ALTER WAREHOUSE
ALTER WAREHOUSE SECOND_WH
SET AUTO_SUSPEND = 60;

--DROP WAREHOUSE
DROP WAREHOUSE SECOND_WH;

--CREATE DATABASE
CREATE OR REPLACE DATABASE FIRST_DB
WITH
COMMENT = "MY FIRST DATABASE";

--RENAME DB
ALTER DATABASE FIRST_DB RENAME TO OUR_FIRST_DB;

--SCHEMA CREATION
CREATE OR REPLACE SCHEMA FIRST_SCHEMA
WITH 
COMMENT = "OUR FIRST SCHEMA";