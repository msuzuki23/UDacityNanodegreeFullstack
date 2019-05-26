import psycopg2 as pg

# Open Connection
connection = pg.connect(user="user", password="pw", host="localhost", port="5432", database="postgres")
cursor = connection.cursor()

# Execute and Fetch Top 3. (Table View top3art)
cursor.execute("SELECT * FROM top3art")
top3 = cursor.fetchall() 

# Check for Empty Results
if top3 != None:
  print("Top 3 Articles:")
  for elem in top3:
    print("Article: {0}, Views: {1}".format(elem[0], elem[1]))
else:
 print("No Articles have been accessed.")

# Close cursor and connection     
cursor.close()
connection.close()