# Must Merge

A demo using Mustache to merge JSON into a template and render the output as either HTML or PDF (via weasyprint).

## Setup

* Python 3 installed.
* Virtual environment created ```python3 -m venv ./env```.
* Activate environment ```source ./env/bin/activate```.
* Install libraries ```pip3 install weasyprint pystache```.

## Usage
JSON is read from std-in so you can pipe commands together to source data from curl.

Result it written to std-out so direct this to the target file (```> out/example.pdf```).

The script itself checks that any mustache variables in the template exist in the JSON from std-in. This to ensure all required values are provided and that the document isn't trying to reference something which doesn't exit.

You can provide as input:
1. ```-m=<mustache_file>``` - The mustache file to be used. **REQUIRED**
1. ```-r=<field,field>``` - Comma delimited list of fields which must be in the template mustache file. **REQUIRED**
1. ```-f=<pdf|html>``` - Only ```pdf``` or ```html``` is supported. Default is ```pdf```.

### Example usage:
```bash
# Explicit output as html
cat in/example.json | python3 mustmerge.py -m=templates/example.mustache -r=name,age -f=html > out/bob.html

# Explicit output as pdf
cat in/example.json | python3 mustmerge.py -m=templates/example.mustache -r=name,age -f=pdf > out/bob.pdf

# Default output format as pdf
cat in/example.json | python3 mustmerge.py -m=templates/example.mustache -r=name,age  > out/bob.pdf

# 'missing' will not be template
cat in/example.json | python3 mustmerge.py -m=templates/example.mustache -r=name,age,missing -f=html

# 'age' will be missing from input
echo '{ "name": "bob"}' | python3 mustmerge.py -m=templates/example.mustache -r=name,age -f=html
```

> Anything else goes wrong like template doesn't exist or input isn't JSON and it just blows up *(and will corrupt the output file if you've directed output there - you have been warned!)*.

Note that ```python3 mustmerge.py``` prints usage instructions as:
```bash
No mustache file or set of required fields input or invalid format type.

Usage: python3 -m=<mustachefile> -r=<required_fields_comma_delim> [-f=<pdf|html>]
JSON data will be read from StdIn, output will be written to StdOut as either html or pdf as requested.

e.g. cat in/example.json | python3 mustmerge.py -m=templates/example.mustache -r=name,age -f=<pdf|html> > out/bob.pdf
```
