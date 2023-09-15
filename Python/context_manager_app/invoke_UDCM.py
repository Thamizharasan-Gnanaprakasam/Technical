from user_defined_cm import SQL_Connection

with SQL_Connection("test.db") as cursor:
    #cursor.execute("create table test(no number,name varchar)")
    #cursor.execute("Insert into test values (1,'Arun'),(2,'Bala')")

    data = cursor.execute("select * from test").fetchall()
    for i in data:
        print(i)