#!/usr/bin/env python2

import psycopg2 as pg

# Open Connection
connection = pg.connect(database="news")
cursor = connection.cursor()

# Execute and Fetch Top 3. (Table View top3art)
cursor.execute("SELECT * FROM top3artic")
top3 = cursor.fetchall()

# Check for Empty Results
if top3 is not None:
  print("Top 3 Articles:")
  for elem in top3:
    print("Article: {0}, Views: {1}".format(elem[0], elem[1]))
else:
  print("No Articles have been accessed.")

# Close cursor and connection
cursor.close()
connection.close()
