import psycopg2 as pg

# Open Connection
connection = pg.connect(user="user", password="pw", host="localhost", port="5432", database="postgres")
cursor = connection.cursor()

# Execute and Fetch Top 3. (Table View top3art)
cursor.execute("SELECT * FROM pop3auth")
top3 = cursor.fetchall() 

# Check for Empty Results
if top3 != None:
  print("Top 3 Arthors:")
  for elem in top3:
    print("Author Name: {0}, Article: {1}, Views: {2}".format(elem[0], elem[1], elem[2]))
else:
 print("No Authors have been viewed at this time.")

# Close cursor and connection     
cursor.close()
connection.close()