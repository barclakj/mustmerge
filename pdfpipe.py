import re
import pystache
import weasyprint
import sys
import json

# Read the mustache file as bytes.
def readMustache(filename):
    data = None
    with open(filename, "r") as f:
        data = f.read()
    return data

# Identifies all the mustache fields in the mustache byte array
def identifyFields(data):
    fields = []
    pattern = r'\{\{.*\}\}'
    entries = re.findall(pattern, data)
    for e in entries:
        v = e[2:len(e)-2]
        fields.append(v)
    return fields

# Checks to ensure fields required in the doc are in the data source values
# and that the document contains the required fields.
def checkFields(vals, fields, mustHave):
    ok = True
    missing = []
    for f in fields:
        if f not in vals or vals[f] is None or vals[f].strip()=='':
            ok = False
            missing.append('Document is looking for field which is not available: ' + f)
    for m in mustHave:
        if m not in fields:
            ok = False
            missing.append('Value is required in document but does not exist: ' + m)
    return ok, missing

# Converts the input stream of json to a dictionary object to merge in
def toDict(js):
    d = json.loads(js)
    return d

# Loads mustache, 
# identifies fields,
# obtains data from stdin,
# checks fields exist in doc and values
# renders mustache as html,
# converts html to pdf,
# and streams the pdf bytes to std out.
def pdfPipeStdInStdOut(mustacheFile, mHaves, format):
    data = readMustache(mustacheFile)
    fields = identifyFields(data)

    line = sys.stdin.read()
    vals = toDict(line)

    state, missing = checkFields(vals, fields, mHaves)

    if not state:
        sys.stderr.write(str(missing) + '\n')
        sys.exit(-1)

    rend = pystache.render(data, vals)

    if format == 'pdf':
        pdfData = weasyprint.HTML(string=rend).write_pdf()
        sys.stdout.buffer.write(pdfData)
    if format == 'html':
        sys.stdout.write(rend)

