import sys
import json
import os

def usage():
    print("Usage: python3 launch_epaxos.py NODE_#")

if __name__ == "__main__":
    file_path = "ips.json"
    file = open(file_path, "r+")
    ips = json.load(file)    

    if len(sys.argv) != 2 :
        usage()

    command = "bin/master -N 3 & bin/server -maddr={} -addr={} -gus=false -e=true -exec=true -dreply=true &"
    if sys.argv[0] == "0":
        os.system(command.format( ips["0"], ips["0"] ))
    elif  sys.argv[1] == "1":
        os.system(command.format( ips["0"], ips["1"] ))
    elif sys.argv[1] == "2":
        os.system(command.format( ips["0"], ips["2"] ))
    else:
        print("Invalid NODE #")
        usage()
