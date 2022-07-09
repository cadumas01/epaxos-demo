import os
import json
import sys

def usage():
    print("Usage: python3 set_delays.py NODE_#")

if __name__ == "__main__":
    file_path = "ips.json"
    file = open(file_path, "r+")
    ips = json.load(file)    

    if len(sys.argv) != 2 :
        usage()

    command = "sudo tc qdisc del dev ens4 root; sudo tc qdisc add dev ens4 root handle 1: htb; sudo tc class add dev ens4 parent 1: classid 1:1 htb rate 1gibps; sudo tc class add dev ens4 parent 1:1 classid 1:2 htb rate 1gibps; sudo tc qdisc add dev ens4 handle 2: parent 1:2 netem delay {}ms sudo tc filter add dev  ens4 pref 2 protocol ip u32 match ip dst {} flowid 1:2; sudo tc class add dev ens4 parent 1: classid 1:1 htb rate 1gibps; sudo tc class add dev ens4 parent 1:1 classid 1:3 htb rate 1gibps; sudo tc qdisc add dev ens4 handle 3: parent 1:3 netem delay {}ms sudo tc filter add dev  ens4 pref 3 protocol ip u32 match ip dst {} flowid 1:3;"    
    if sys.argv[1] == "0":
        os.system(command.format( "36", ips["1"],"75.5", ips["2"] ))
    elif  sys.argv[1] == "1":
        os.system(command.format( "36", ips["0"],  "44", ips["2"] ))
    elif sys.argv[1] == "2":
        os.system(command.format( "75.5", ips["0"], "44", ips["1"],))
    else:
        print("Invalid NODE #")
        usage()


