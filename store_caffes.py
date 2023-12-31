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
mycursor = mydb.cursor()
mycursor.execute("DROP TABLE IF EXISTS sweets")
mycursor.execute("DROP TABLE IF EXISTS caffes")

mycursor.execute("CREATE TABLE caffes ("
                    "id INT NOT NULL AUTO_INCREMENT,"
                    "name VARCHAR(255) CHARACTER SET utf8mb4,"
                    "address VARCHAR(255) CHARACTER SET utf8mb4,"
                    "latitude FLOAT(23),"
                    "longitude FLOAT(23),"
                    "PRIMARY KEY (id))")
mycursor.execute("CREATE TABLE sweets ("
                    "id INT NOT NULL AUTO_INCREMENT,"
                    "caffe_id INT NOT NULL,"
                    "original_id INT NOT NULL,"
                    "name VARCHAR(255) CHARACTER SET utf8mb4,"
                    "price FLOAT(23),"
                    "serving FLOAT(23),"
                    "plate_area FLOAT(23),"
                    "sourcing VARCHAR(31) CHARACTER SET utf8mb4,"
                    "started_producing INT,"
                    "type VARCHAR(31) CHARACTER SET utf8mb4,"
                    "with_brown_sugar TINYINT,"
                    "with_nuts TINYINT,"
                    "whole_weat_flour TINYINT,"
                    "with_eggs TINYINT,"
                    "with_icing TINYINT,"
                    "lactose_free TINYINT,"
                    "with_cocoa TINYINT,"
                    "with_berries TINYINT,"
                    "look_date DATE,"
                    "PRIMARY KEY (id),"
                    "FOREIGN KEY (caffe_id) REFERENCES caffes(id))")

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

sweets_path = "./data_exported/sweets.csv"
if os.path.exists(sweets_path):
    sweets_df = pd.read_csv(sweets_path, index_col=0)
    sweets_df.to_sql('sweets', con=engine, if_exists='append', index=False)
else:
    print(f"Cannot find sweets entries in {sweets_path}. The table will not be created.")