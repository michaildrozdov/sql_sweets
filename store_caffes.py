import argparse
import mysql.connector
from sqlalchemy import create_engine
import os
import pandas as pd

description = "Load all CSV of format 'caffes_anywhere.csv' from the exported data directory."\
              "User and password should be provided as input parameters of the scripts."
data_dir = "./data_exported/"

parser = argparse.ArgumentParser(description=description,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("user", help="user of the SQL server")
parser.add_argument("password", help="password for the user")

args = parser.parse_args()

# Housekeeping - create the db or clear the table if it is already there.
# Can't just drop it as it may contain references used by the other table.
mydb = mysql.connector.connect(
  host="localhost",
  user=args.user,
  password=args.password
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS sweets_database")
mydb = mysql.connector.connect(
      host="localhost",
      user=args.user,
      password=args.password,
      database="sweets_database"
    )
mycursor = mydb.cursor(buffered=True)
mycursor.execute("SHOW TABLES")

has_caffes_table = False
for table in mycursor:
    if table[0] == "caffes":
        has_caffes_table = True
        break
if has_caffes_table:
    print("Clearing the table")
    
    # Remove all explicitly, at least on MySQL Server 8.1 auto-increment index starts with 1
    mycursor.execute("DELETE FROM caffes WHERE id > 0;")
    mycursor.execute("ALTER TABLE caffes AUTO_INCREMENT=1;")
else:
    mycursor.execute("CREATE TABLE caffes ("
                        "id INT NOT NULL AUTO_INCREMENT,"
                        "name VARCHAR(255) CHARACTER SET utf8mb4,"
                        "address VARCHAR(255) CHARACTER SET utf8mb4,"
                        "latitude FLOAT(23),"
                        "longitude FLOAT(23),"
                        "PRIMARY KEY (id))")


all_files_names = os.listdir(data_dir)
data_frames = []          
for filename in all_files_names:
    if filename.find("caffes") < 0 or filename.find(".csv") < 0:
        continue
    df = pd.read_csv(data_dir + filename, index_col=0)
    data_frames.append(df)
    
all_caffes = pd.concat(data_frames, ignore_index=True)
all_caffes.reset_index(drop=True)
#all_caffes = all_caffes.drop(all_caffes.columns[0], axis=1)

debug_caffes = False
if debug_caffes:
    import sys
    specific_caffe = all_caffes.iloc[0]
        
    #print(specific_caffe)
    print(all_caffes)
    print(specific_caffe['name'])
    print(all_caffes.index.tolist())
    
    print(list(all_caffes))
    sys.exit()
    
# Close the connection because a different kind will be created
mycursor.close()
mydb.close()

engine = create_engine(f"mysql+mysqlconnector://{args.user}:{args.password}@localhost/sweets_database")
print("Adding entries")
all_caffes.to_sql('caffes', con=engine, if_exists='append', index=False)