#!/usr/bin/env python2

import psycopg2 as pg

# Open Connection
connection = pg.connect(database="news")
cursor = connection.cursor()

# Execute and Fetch top 1%
cursor.execute("SELECT * FROM dayError1Perc")
top3 = cursor.fetchall()

# Check for Empty Results
if top3 is not None:
  print("Day(s) with More than 1 Percent Error (\"400 NOT FOUND\"):")
  for elem in top3:
    print("Date: {0}, Error Count: {1}, ".format(elem[0], elem[1])+
          "Total Access: {0}, Error Perc: {1}%".format(elem[2], elem[3]))
else:
  print("No Errors have been logged at this time.")

# Close cursor and connection
cursor.close()
connection.close()
