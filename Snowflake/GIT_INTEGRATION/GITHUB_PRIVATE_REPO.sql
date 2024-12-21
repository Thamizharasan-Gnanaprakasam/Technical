USE ROLE ACCOUNTADMIN ;

CREATE OR REPLACE SECRET my_github_secret
TYPE = PASSWORD
USERNAME = 'Thamizharasan-Gnanaprakasam'
PASSWORD = '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';

SHOW SECRETS;

CREATE OR REPLACE API INTEGRATION my_github_api_integration
API_PROVIDER = git_https_api
API_ALLOWED_PREFIXES = ('https://github.com/Thamizharasan-Gnanaprakasam')
ALLOWED_AUTHENTICATION_SECRETS = (my_github_secret)
ENABLED = TRUE;

show integrations;

CREATE OR REPLACE GIT REPOSITORY my_github_repo
API_INTEGRATION = my_github_api_integration
GIT_CREDENTIALS = my_github_secret
ORIGIN = 'https://github.com/Thamizharasan-Gnanaprakasam/Technical';

SHOW GIT REPOSITORIES;

SHOW GIT BRANCHES IN GIT REPOSITORY my_github_repo;

LS @my_github_repo/branches/main;