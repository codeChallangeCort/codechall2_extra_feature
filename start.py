import pandas as pd
import json
import sys
import re

# script would take args as filename.csv."

parsed_files = []

while True:
    try:
        option = input("Please enter a file name or 'N': ")
        if option not in ["N","n"]:
            parsed_files.append(option)
        else:
            break
    except Exception as e:
        print(e)

print(f"\n{len(parsed_files)} PARSED FILES: ", parsed_files)
# Empty Dictionary for JSON dumps

json_data = {}

# List of customers information including first_name, last_name and email.

json_data["user_list"] = []

# list_id will start from 0

list_id = 0

# user_list_size is the count of customer 

json_data["user_list_size"] = 0

regex = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

email_list = []

def getInfo(row):
    """
    This FUncation will split the full name in firstname and lastname, with list_id, and will dump that information in temporary dict
    and temp dict into a list of
    json_data
    """

    # json_temp is to get the info for a individual customer for temporary time.

    json_temp = {}
    global list_id

    if re.search(regex,row["email"]):
        if row["email"] not in email_list:

            list_id += 1
            json_temp["list_id"] = list_id
            json_temp["email"] = row["email"]
            if " " in str(row["full_name"]) and len(row["full_name"]) >= 3:
                full_name = row["full_name"].split(" ")
                json_temp["first_name"] = full_name[0]
                json_temp["last_name"] = full_name[1]
            else:
                json_temp["first_name"] = "Customer"
                json_temp["last_name"] = "N/A"
            email_list.append(row["email"])
            json_data["user_list"].append(json_temp)
        else:
            print("Duplicate found: ", row["full_name"], row["email"])
    else:
        print("Invalid Information: ", row["full_name"], row["email"])


if __name__ == "__main__":
    
    missing_file = []
    for parsed_file in parsed_files:
        try:
            df = pd.read_csv(parsed_file)
            df.apply(lambda x: getInfo(x), axis=1)

        except Exception as e:
            missing_file.append(parsed_file)
        continue

    print(f"{len(missing_file)} MISSING FILES: ", missing_file) if len(missing_file) > 0 else print("All Files Found")
    json_data["user_list_size"] = list_id

    if list_id > 0:
        with open('results.json', 'w') as outfile:
            json.dump(json_data, outfile, indent=4)
