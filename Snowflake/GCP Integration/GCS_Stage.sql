CREATE OR REPLACE FILE FORMAT MANAGE_DB.FILE_FORMATS.GCP_FILEFORMAT_CSV
TYPE = CSV,
FIELD_DELIMITER = ',',
SKIP_HEADER = 1,
FIELD_OPTIONALLY_ENCLOSED_BY = '"',
NULL_IF = ('NULL','null'),
EMPTY_FIELD_AS_NULL = TRUE;

CREATE OR REPLACE STAGE MANAGE_DB.EXTERNAL_STAGES.GCP_STAGE_CSV
URL = 'gcs://snowflakegcp-bucket',
STORAGE_INTEGRATION = GCP_INT,
FILE_FORMAT = MANAGE_DB.FILE_FORMATS.GCP_FILEFORMAT_CSV;

LS @MANAGE_DB.EXTERNAL_STAGES.GCP_STAGE_CSV;

--JSON

CREATE OR REPLACE FILE FORMAT MANAGE_DB.FILE_FORMATS.GCP_FILEFORMAT_JSON
TYPE = JSON;

CREATE OR REPLACE STAGE MANAGE_DB.EXTERNAL_STAGES.GCP_STAGE_JSON
URL = 'gcs://snowflakegcp-bucket-json',
STORAGE_INTEGRATION = GCP_INT,
FILE_FORMAT = MANAGE_DB.FILE_FORMATS.GCP_FILEFORMAT_JSON;

LS @MANAGE_DB.EXTERNAL_STAGES.GCP_STAGE_JSON;