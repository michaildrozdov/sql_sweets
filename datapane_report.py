import argparse
import datapane as dp
import mysql.connector
import pandas as pd
import datetime
import plotly.express as px

description = "Create a report from the database."

parser = argparse.ArgumentParser(description=description,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("user", help="user of the SQL server")
parser.add_argument("password", help="password for the user")

args = parser.parse_args()

mydb = mysql.connector.connect(
  host="localhost",
  user=args.user,
  password=args.password,
  database="sweets_database"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT look_date, avg(price) from sweets GROUP BY look_date ORDER BY look_date ASC;")

result = mycursor.fetchall()
as_float = []
for r in result:
    as_float.append((r[0].strftime("%Y-%m-%d"), float(r[1])))

df = pd.DataFrame(as_float, columns = ['look date', 'average price'])
print(df)

fig = px.line(df, 
             y = 'average price', 
             x = 'look date',
             text = 'average price',
             orientation = 'v')

view = dp.Blocks(
    dp.Plot(fig),
    dp.DataTable(df)
)

dp.save_report(view, path="sweet_report.html")
