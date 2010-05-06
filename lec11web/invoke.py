#!/usr/bin/env python
import sys, os

server = "phylo.bio.ku.edu"
port_str = ":5000"


otherargs=[('return_raw_content', 'True'),
            ('blocking', 'True')]
service = None
inputFile = None
for arg in sys.argv[1:]:
    if arg == "-d":
        server = "127.0.0.1"
    elif arg.startswith("-k"):
        kv = arg[2:].split('=')
        if len(kv) < 2:
            sys.exit("Expecting a key=value pair for after the -k flag")
        k = kv[0]
        v = "=".join(kv[1:])
        t = (k,v)
        otherargs.append(t)
    elif service is None:
        service = arg
    elif inputFile is None:
        inputFile = os.path.abspath(arg)
    else:
        sys.exit("Expecting two arguments a service and a path to a file")

if inputFile is None:
    sys.exit("Expecting two arguments a service and a path to a file")

if not os.path.exists(inputFile):
    sys.exit("%s does not exist" % inputFile)
    
import pycurl
c = pycurl.Curl()
c.setopt(c.POST, 1)
c.setopt(c.URL, server + port_str + "/" + service + "/uploaded")
c.setopt(c.HTTPPOST, [("file", (pycurl.FORM_FILE, inputFile))] + otherargs)
c.perform()
rc = c.getinfo(pycurl.RESPONSE_CODE)
c.close()
if rc < 200 or rc >= 300:
    sys.exit("Error. Response code = %s" % str(rc))
