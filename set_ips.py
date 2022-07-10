import json
import sys
import os
import subprocess
from textwrap import indent

# run via:
# python update_config <config_num> <protocol>

if len(sys.argv) != 4:
    print("Usage: python3 set_ips <INTERNAL_IP_CALIFORNIA> <INTERNAL_IP_VIRGINIA> <INTERNAL_IP_IRELAND>")
    exit(1)

file_path = "ips.json"
file = open(file_path, "r+")
json_object = json.load(file)
file.close()

servers = ["0", "1", "2"]

for i in range(0,3):
    json_object[servers[i]] = sys.argv[i + 1]

file = open(file_path, "w")
json.dump(json_object, file, indent=4)

file.close()

