/* 
Time Travel - we can do a time travel on table for upto 90 days in enterprise edition and 1 day in standard edition

3 ways we can do time travel
    1. based on seconds - offset => secs
    2. based on time - timestamp => 'timestamp'
    3. based on query id - statement => 'queryid'
We can do time travel to the exact time using at keyword or before the time stamp we specified using before keyword
*/

CREATE OR REPLACE TABLE OUR_FIRST_DB.public.test (
   id int,
   first_name string,
  last_name string,
  email string,
  gender string,
  Job string,
  Phone string);
    


CREATE OR REPLACE FILE FORMAT MANAGE_DB.file_formats.csv_file
    type = csv
    field_delimiter = ','
    skip_header = 1;
    
CREATE OR REPLACE STAGE MANAGE_DB.external_stages.time_travel_stage
    URL = 's3://data-snowflake-fundamentals/time-travel/'
    file_format = MANAGE_DB.file_formats.csv_fileformat;
    


LIST @MANAGE_DB.external_stages.time_travel_stage;



COPY INTO OUR_FIRST_DB.public.test
from @MANAGE_DB.external_stages.time_travel_stage
files = ('customers.csv');

SELECT * FROM OUR_FIRST_DB.public.test;

UPDATE OUR_FIRST_DB.public.test SET LAST_NAME = 'JOHN';

SELECT * FROM OUR_FIRST_DB.public.test AT (OFFSET => -60*2); -- TRAVEL BASED ON SECONDS
SELECT * FROM OUR_FIRST_DB.public.test BEFORE (OFFSET => -60*2); -- TRAVEL BASED ON SECONDS

SELECT CURRENT_TIMESTAMP; --2023-09-22 08:14:08.889 -0700
SHOW PARAMETERS;
ALTER SESSION SET TIMEZONE = 'UTC';
SELECT CURRENT_TIMESTAMP; --2023-09-22 15:16:41.201 +0000

ALTER SESSION SET TIMEZONE = 'America/Los_Angeles';
SELECT CURRENT_TIMESTAMP; --2023-09-22 08:17:30.344 -0700


CREATE OR REPLACE TABLE OUR_FIRST_DB.public.test (
   id int,
   first_name string,
  last_name string,
  email string,
  gender string,
  Job string,
  Phone string);
    


CREATE OR REPLACE FILE FORMAT MANAGE_DB.file_formats.csv_file
    type = csv
    field_delimiter = ','
    skip_header = 1;
    
CREATE OR REPLACE STAGE MANAGE_DB.external_stages.time_travel_stage
    URL = 's3://data-snowflake-fundamentals/time-travel/'
    file_format = MANAGE_DB.file_formats.csv_fileformat;
    


LIST @MANAGE_DB.external_stages.time_travel_stage;



COPY INTO OUR_FIRST_DB.public.test
from @MANAGE_DB.external_stages.time_travel_stage
files = ('customers.csv');

SELECT * FROM OUR_FIRST_DB.public.test;

UPDATE OUR_FIRST_DB.public.test SET JOB = 'HEALTH';

SELECT * FROM OUR_FIRST_DB.public.test BEFORE (TIMESTAMP => '2023-09-22 15:19:00'::TIMESTAMP); -- TIMESTAMP IN UTC


CREATE OR REPLACE TABLE OUR_FIRST_DB.public.test (
   id int,
   first_name string,
  last_name string,
  email string,
  gender string,
  Job string,
  Phone string);

COPY INTO OUR_FIRST_DB.public.test
from @MANAGE_DB.external_stages.time_travel_stage
files = ('customers.csv');

SELECT * FROM OUR_FIRST_DB.public.test;

UPDATE OUR_FIRST_DB.public.test SET LAST_NAME = 'JOHN'; --01af295c-0604-c01f-0000-ff5b000140aa

SELECT * FROM OUR_FIRST_DB.public.test BEFORE (STATEMENT => '01af295c-0604-c01f-0000-ff5b000140aa');


