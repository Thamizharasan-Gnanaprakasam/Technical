SHOW SHARES;

orb36303;

DESC SHARE orb36303.ORDERS_SHARE;

CREATE OR REPLACE DATABASE DATA_S FROM SHARE orb36303.ORDERS_SHARE;

DESC SHARE ORDERS_SHARE;

SELECT * FROM DATA_S.PUBLIC.ORDERS;