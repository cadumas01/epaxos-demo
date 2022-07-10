import sys
import json
import os

def usage():
    print("Usage: python3 launch_epaxos.py NODE_# TRUE_FOR_PAXOS")

if __name__ == "__main__":
    file_path = "ips.json"
    file = open(file_path, "r+")
    ips = json.load(file)    

    if len(sys.argv) < 2 or len(sys.argv) > 3 :
        usage()

    
    command = ""
    if sys.argv[2].lower() == "true":
         command = "bin/master {} & bin/server -maddr={} -addr={} -gus=false -exec=true {} &"
    else:
        command = "bin/master {} & bin/server -maddr={} -addr={} -gus=false -e=true -exec=true {} &"
    
    if sys.argv[1] == "0":
        os.system(command.format( "-N 3", ips["0"], ips["0"], "-dreply=true" ))
    elif  sys.argv[1] == "1":
        os.system(command.format( "", ips["0"], ips["1"], "" ))
    elif sys.argv[1] == "2":
        os.system(command.format( "", ips["0"], ips["2"], "" ))
    else:
        print("Invalid NODE #")
        usage()
