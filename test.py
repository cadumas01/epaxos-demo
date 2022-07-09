import os

def usage():
    print("Usage: python3 test.py WRITE_PERC CONFLICT_RATE TOTAL_NUMBER_CLIENTS")

if __name__ == "__main__":
    if len(sys.args) != 4:
        usage()

    args = sys.args
    command = "timeout 180s bin/client"

    file = open(file_path, "r+")
    ips = json.load(file)

    command += " -maddr="+ips["0"]
    command += " -writes="+ args[1]
    command += " -c="+args[2]
    command += " -T="+args[3]+" -forceLeader=0"

    os.system(command)   
    os.system(python3 client_metrics.py)
