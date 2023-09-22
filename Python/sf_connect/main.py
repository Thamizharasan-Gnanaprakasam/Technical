import snowflake.connector, os # NOQA

con = snowflake.connector.connect(user='tamil',
                                  password = 'Ayla@23#',
                                  #authenticator = 'oauth',
                                  #token = 'token',
                                  account = 'orb36303.us-east-1',
                                  role = 'ACCOUNTADMIN',
                                  warehouse = 'COMPUTE_WH',
                                  database = 'OUR_FIRST_DB',
                                  schema = 'PUBLIC',
                                  login_timeout = 200,
                                  network_timeout = 200,
                                  autocommit = False)

cursor = con.cursor()

cursor.execute("select * from OUR_FIRST_DB.PUBLIC.EMPLOYEES1 LIMIT 10")

for i in cursor.fetchall():
    print(i)

con.close()