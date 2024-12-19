CREATE WAREHOUSE KAMESH_DEMO_S;

USE WAREHOUSE KAMESH_DEMOS_S;

CREATE DATABASE KAMESH_GIT_REPOS;

USE DATABASE KAMESH_GIT_REPOS;

CREATE SCHEMA GITHUB;

USE SCHEMA GITHUB;

--API INTEGRATION

CREATE OR REPLACE API INTEGRATION KAMESHSAMPATH_GIT
API_PROVIDER = git_https_api
API_ALLOWED_PREFIXES = ('https://github.com/kameshsampath')
enabled = TRUE;

--GIT REPOSITORY
CREATE OR REPLACE GIT REPOSITORY GIT_INTEGRATION_DEMO
API_INTEGRATION = KAMESHSAMPATH_GIT
origin = 'https://github.com/kameshsampath/sf-git-integration-demo.git';

--REFRESH LOCAL REPO
ALTER GIT REPOSITORY GIT_INTEGRATION_DEMO FETCH;

--list the files
LS @GIT_INTEGRATION_DEMO/branches/main;

EXECUTE IMMEDIATE FROM @git_integration_demo/branches/main/demo.sql;


--WITH CREDENTIALS
CREATE OR REPLACE API INTEGRATION TAMIL_GIT
api_provider = git_https_api
api_allowed_prefixes = ('https://github.com/kameshsampath')
enabled = true
ALLOWED_AUTHENTICATION_SECRETS = ALL;

CREATE OR REPLACE SECRET PASS
TYPE = PASSWORD
USERNAME = 'Thamizharasan-Gnanaprakasam'
PASSWORD = 'Ayla@23#';

CREATE OR REPLACE GIT REPOSITORY git_int_demo
API_INTEGRATION = TAMIL_GIT
GIT_CREDENTIALS = PASS
origin = 'https://github.com/kameshsampath/sf-git-integration-demo.git';

ALTER GIT REPOSITORY git_int_demo FETCH;

ls @git_int_demo/branches/main;

EXECUTE IMMEDIATE FROM @git_int_demo/branches/main/demo.sql;