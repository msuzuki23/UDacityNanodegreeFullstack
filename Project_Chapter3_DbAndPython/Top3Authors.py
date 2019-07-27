#!/usr/bin/env python2

import psycopg2 as pg

# Open Connection
connection = pg.connect(database="news")
cursor = connection.cursor()

# Execute and Fetch Top 3 authors
cursor.execute("SELECT * FROM pop3auth")
top3 = cursor.fetchall()

# Check for Empty Results
if top3 is not None:
  print("Top 3 Arthors:")
  for elem in top3:
    print("Author Name: {0}, Article: {1}, ".format(elem[0], elem[1])+
          "Views: {0}".format(elem[2]))
else:
  print("No Authors have been viewed at this time.")

# Close cursor and connection
cursor.close()
connection.close()
