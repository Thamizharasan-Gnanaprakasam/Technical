CREATE OR REPLACE DATABASE BITBUCKET;

CREATE OR REPLACE SCHEMA PUBLIC;

CREATE OR REPLACE SECRET my_bb_secret
TYPE = PASSWORD
USERNAME = 'thamizharasangnanaprakas-admin'
PASSWORD = 'ATBBX47HsUgvymxpbm3EJbENKHgF5F5019D3';

--git clone https://thamizharasangnanaprakas-admin@bitbucket.org/thamizharasangnanaprakasam/my_private_repo.git

CREATE OR REPLACE API INTEGRATION my_bb_api
API_PROVIDER = GIT_HTTPS_API
API_ALLOWED_PREFIXES = ('https://bitbucket.org/thamizharasangnanaprakasam')
ALLOWED_AUTHENTICATION_SECRETS = (my_bb_secret)
ENABLED = TRUE;

CREATE OR REPLACE GIT REPOSITORY my_bb_repo
API_INTEGRATION = my_bb_api
ORIGIN = 'https://bitbucket.org/thamizharasangnanaprakasam/my_private_repo'
GIT_CREDENTIALS = my_bb_secret;
