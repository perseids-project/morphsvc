import os, requests, sys, re
from urllib import parse


fixture = os.path.join(os.path.dirname(__file__), 'tests', 'r1')
failed = os.path.join(os.path.dirname(__file__), 'tests', 'failed')
success = os.path.join(os.path.dirname(__file__), 'tests', 'success')
errors = os.path.join(os.path.dirname(__file__), 'tests', 'errors')
#host = "http://bsp.perseids.org/bsp/morphologyservice"
host = "http://localhost:5000"
in_file = open(fixture, 'r')
out_failed = open(failed, 'w')
out_success = open(success, 'w')
out_errored = open(errors, 'w')
for line in in_file.readlines():
    #line = parse.unquote(line)
    url = host + line.strip()
    print(url)
    resp = requests.get(url, headers= { 'Accept': 'application/json'})
    resp.encoding = "utf-8"
    print(resp.text)
    p = re.compile("Body",flags=re.M)
    parsed = resp.json()
    try:
        resp.raise_for_status()
        if p.search(resp.text):
            out_success.write("Request=" + line + "\nResponse=\n")
            out_success.write(resp.text + "\n")
        else:
            out_failed.write("Request=" + line + "\nResponse=\n")
            out_failed.write(resp.text + "\n")
    except:
        out_errored.write("Request=" + line + "\nResponse=\n")
        out_errored.write(resp.text + "\n")

