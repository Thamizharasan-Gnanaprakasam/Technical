USE ROLE SYSADMIN;

CREATE WAREHOUSE EXERCISE_WH
WAREHOUSE_SIZE = XSMALL
AUTO_SUSPEND = 600  -- automatically suspend the virtual warehouse after 10 minutes of not being used
AUTO_RESUME = TRUE 
COMMENT = 'This is a virtual warehouse of size X-SMALL that can be used to process queries.';

DROP WAREHOUSE EXERCISE_WH;