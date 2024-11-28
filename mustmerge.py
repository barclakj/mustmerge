
import sys
import pdfpipe as pipe

mustacheFile = None
mHaves = None
format = 'pdf'

for arg in sys.argv:
    if arg.startswith('-m='):
        mustacheFile = arg[3:]
    if arg.startswith('-r='):
        required=arg[3:]
        mHaves = required.split(',')
    if arg.startswith('-f='):
        format=arg[3:]
        if format not in ('pdf','html'):
            sys.stderr.write('Invalid format! ' + format + '\n')
            format = None
    
if mustacheFile is None or mHaves is None or format is None:
    sys.stderr.write('No mustache file or set of required fields input or invalid format type.\n\n')
    sys.stderr.write('Usage: python3 -m=<mustachefile> -r=<required_fields_comma_delim> [-f=<pdf|html>]\n')
    sys.stderr.write('JSON data will be read from StdIn, output will be written to StdOut as either html or pdf as requested.\n\n')
    sys.stderr.write('e.g. cat in/example.json | python3 mustmerge.py -m=templates/example.mustache -r=name,age -f=<pdf|html> > out/bobs_age.pdf\n')
    sys.exit(-1)

# {"name": "bob", "age": "123"}

pipe.pdfPipeStdInStdOut(mustacheFile, mHaves, format)

