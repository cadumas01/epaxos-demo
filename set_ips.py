import json
import sys
import os
import subprocess
from textwrap import indent

# run via:
# python update_config <config_num> <protocol>

# updates a json file
def update(file_path, key, new_value):
    file = open(file_path, "r+")
    json_object = json.load(file)
    

    json_object[key] = new_value

    file = open(file_path, "w")
    json.dump(json_object, file, indent=4)
    # file.write(simplej)

    file.close()


print("Called set_ips.py")
if len(sys.args) != 4:
    print("Usage: python3 set_ips <INTERNAL_IP_CALIFORNIA> <INTERNAL_IP_VIRGINIA> <INTERNAL_IP_IRELAND>")
    exit(1)

file = open(file_path, "r+")
json_object = json.load(file)
file.close()

servers = ["1", "2", "3"]

for i in range(0,3):
    json_object[server[i]] = os.args[i + 1]
    print("Just set " , server[i])


file = open(file_path, "w")
json.dump(json_object, file, indent=4)

file.close()

