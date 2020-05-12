import mysql.connector
db_connection = mysql.connector.connect(
  host="aws-surf-data.cwc6jybwwwrj.us-east-1.rds.amazonaws.com",
  user="admin",
  passwd="xxmaster",
    database="surf_data"
)
db_cursor = db_connection.cursor()
sqlQuery = "SELECT * FROM surf_data_testing;"
db_cursor.execute(sqlQuery)
result = db_cursor.fetchall()
for x in result:
    print(x)
print(db_connection)