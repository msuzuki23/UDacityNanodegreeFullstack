import psycopg2 as pg

# Open Connection
connection = pg.connect(user="user", password="pw", host="localhost", port="5432", database="postgres")
cursor = connection.cursor()

# Execute and Fetch Top 3. (Table View top3art)
cursor.execute("SELECT * FROM dayError1Perc")
top3 = cursor.fetchall() 

# Check for Empty Results
if top3 != None:
  print("Day(s) with More than 1 Percent Error (\"400 NOT FOUND\"):")
  for elem in top3:
    print("Date: {0}, Count Errors: {1}, Total Accesses: {2}, Error Percentage: {3}%".format(elem[0], elem[1], elem[2], elem[3]))
else:
 print("No Errors have been logged at this time.")

# Close cursor and connection     
cursor.close()
connection.close()