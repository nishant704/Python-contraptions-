#!/usr/bin/python
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

# start a new nmap scan on localhost with some specific options
def do_scan(targets, options):
    parsed = None
    nmproc = NmapProcess(targets, options)
    rc = nmproc.run()
    if rc != 0:
        print("nmap scan failed: {0}".format(nmproc.stderr))
#    print(type(nmproc.stdout))

    try:
        parsed = NmapParser.parse(nmproc.stdout)
    except NmapParserException as e:
        print("Exception raised while parsing scan: {0}".format(e.msg))
    return parsed


# print scan results from a nmap report
def print_scan(nmap_report):
    print("Starting Nmap {0} at {1}".format(nmap_report.version,nmap_report.started))
    version=nmap_report.version
    state=nmap_report.started
    for host in nmap_report.hosts:
        if len(host.hostnames):
            tmp_host = host.hostnames.pop()
        else:
            tmp_host = host.address

        print("Nmap scan report for {0} ({1})".format(tmp_host,host.address))
        print("Host is {0}.".format(host.status))
       
        for osmatch in host.os.osmatches: #NmapParser manipulation to detect OS and accuracy of detection.
          os = osmatch.name
          accuracy = osmatch.accuracy
          print "Operating System Guess: ", os, "- Accuracy Detection", accuracy
          break

        print("  PORT     STATE         SERVICE")

        for serv in host.services:
            pserv = "{0:>5s}/{1:3s}  {2:12s}  {3}".format(str(serv.port),serv.protocol,serv.state,serv.service)
            if len(serv.banner):
                pserv += " ({0})".format(serv.banner)
            print(pserv)
 
    print(nmap_report.summary)

if __name__ == "__main__":
    with open('vpc_hosts.conf') as f:
        ipList = [line.split()[0] for line in f]
        hostname = [line.split()[1] for line in f]
    	for ip in ipList:
            report = do_scan(ip, "--open -A -sV -O --osscan-guess -oX scanme2.xml")
            if report:
               print_scan(report)
            else:
              print("No results returned")
