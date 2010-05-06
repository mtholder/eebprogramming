#!/usr/bin/env python

# this should work if you have urllib2_file installed from git://github.com/mtholder/urllib2_file.git

import sys, os

if 'SERVER' in os.environ:
    server = os.environ.get('SERVER')
else:
    server = "phylo.bio.ku.edu"
port_str = ":5000"


service = None
input_file = None

post_data = {'return_raw_content' : 'True', #MTH web-service convention. Not Generic!
            'blocking' : 'True', #MTH web-service convention. Not Generic!
            }

for arg in sys.argv[1:]:
    if arg == "-d":
        server = "127.0.0.1"
    elif arg.startswith("-k"):
        kv = arg[2:].split('=')
        if len(kv) < 2:
            sys.exit("Expecting a key=value pair for after the -k flag")
        k = kv[0]
        v = "=".join(kv[1:])
        post_data[k] = v
    elif service is None:
        service = arg
    elif input_file is None:
        input_file = os.path.abspath(arg)
    else:
        sys.exit("Expecting two arguments a service and a path to a file")

if input_file is None:
    sys.exit("Expecting two arguments a service and a path to a file")

if not os.path.exists(input_file):
    sys.exit("%s does not exist" % input_file)


key = "file" #MTH web-service convention. Not Generic!
post_data["file"] = {   'fd' : open(input_file, 'rU'),
                        'filename' : os.path.split(input_file)[-1] }
import urllib2_file
import urllib2
url = 'http://' + server + port_str +  urllib2.quote("/" + service + "/uploaded")



try:
    response = urllib2.urlopen(url, post_data)
except urllib2.HTTPError, x:
    ex = x
    if x.code == 404:
        sys.stderr.write("""HTTP Error Code: 404
You got the dreaded 404 code meaning that the server could not find the resource
that you were requesting.  Make sure that the service name 
"%s" is spelled correctly.  
Also check that the host serves the "uploaded" POST interface used by the 
Holder lab at:
    %s
Below is the 404 message from the server in the off chance that it gives you any
clues:
"%s"
""" % (service, x.url, str(x)))
    else:
        sys.stderr.write("HTTP Error code: %d\n%s\n" % (x.code, str(x)))
    sys.exit(x.code)
else:
    print response.read()

 
