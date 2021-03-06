#! /usr/bin/python3
# encode:utf-8
import subprocess
import sys
import json
from socket import gethostname
import datetime

def main():
    cmdSar = ["/usr/bin/sar", "1", "1"]
    cmdLoadAvg = ["/usr/bin/sar", "-q", "1", "1"]
    cmdFree = ["/usr/bin/free"]

    copSar = subprocess.check_output(cmdSar, stderr=subprocess.STDOUT).decode("utf-8")
    copLA = subprocess.check_output(cmdLoadAvg, stderr=subprocess.STDOUT).decode("utf-8")
    copFree = subprocess.check_output(cmdFree, stderr=subprocess.STDOUT).decode("utf-8")
    
    rsltHost = gethostname()
    rsltDate = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    rsltSar = copSar.strip().split("\n")[3].strip().split()
    rsltLoadAvg = copLA.strip().split("\n")[3].strip().split()
    rsltFree1 = copFree.strip().split("\n")[1].strip().split()
    rsltFree2 = copFree.strip().split("\n")[2].strip().split()
        
    rsltCpu = {
        "LoadAvg1":float(rsltLoadAvg[3]),
        "LoadAvg5":float(rsltLoadAvg[4]),
        "LoadAvg15":float(rsltLoadAvg[5]),
        "User":float(rsltSar[2]),
        "System":float(rsltSar[4]),
        "IOWait":float(rsltSar[5]),
        "Idle":float(rsltSar[7])
    }
    
    rsltMem = {
        "Total":int(rsltFree1[1]),
        "Used":int(rsltFree2[2]),
        "Free":int(rsltFree2[3])
    }
    
    objAll = json.dumps({
        "Hostname": rsltHost, 
        "Date":rsltDate,
        "CpuData": rsltCpu,
        "MemData":rsltMem
    })

    print('HTTP/1.1 200 OK')
    print('Content-Type: application/json')
    print('Content-Length: {}'.format(len(objAll) + 1))
    print("")
    print(objAll)
    
if __name__ == '__main__':
  main()

