import pandas as pd
import json
import sys
import re


# script would take args as filename.csv."

try:
    parsed_files = []
    for each_file in sys.argv[1:]:  
        parsed_files.append(each_file)
    print("Total Files parsed: ", parsed_files)   
except Exception as e:
    sys.exit()

# Empty Dictionary for JSON dumps

json_data = {}

# List of customers information including first_name, last_name and email.

json_data["user_list"] = []

# list_id will start from 0

list_id = 1

# user_list_size is the count of customer 

json_data["user_list_size"] = 0


regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def getInfo(row):
    """
    This FUncation will split the full name in firstname and lastname, with list_id, and will dump that information in temporary dict
    and temp dict into a list of
    json_data
    """ 

    # json_temp is to get the info for a individual customer for temporary time.
    
    json_temp = {}
    global list_id
    json_temp["list_id"] = list_id
    
    if " " in str(row["full_name"]) and re.search(regex,row["email"]):
        full_name = row["full_name"].split(" ")
        json_temp["first_name"] = full_name[0]
        json_temp["last_name"] = full_name[1]
    else:
        json_temp["first_name"] = row["full_name"]
        json_temp["last_name"] = "N/A"
    json_temp["email"] = row["email"]

    # json_temp will be appended into the list of json_data.

    json_data["user_list"].append(json_temp)
    list_id += 1
    
# If more than one filesname has been passed with "," then for each file data would be readed and stored into json_data.
    
for parsed_file in parsed_files:
    df = pd.read_csv(parsed_file)
    json_data["user_list_size"] += len(df)
    df.apply(lambda x: getInfo(x), axis=1)

# To dump the json_data into result.json.

with open('results.json', 'w') as outfile:
    json.dump(json_data, outfile, indent=4)
