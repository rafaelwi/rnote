# RANDF Processor: Takes a raw file and converts it to a compiled document.

import argparse
import randf_cliargs as cliargs
import randf_generator as gen
import randf_parser as parser
import sys
import os
from xhtml2pdf import pisa

### Main Program ###
arg_parser = argparse.ArgumentParser()
cliargs.addArgs(arg_parser)
args = arg_parser.parse_args()

# Get the cl args
if args.input:
    print("Input file: " + args.input)
else:
    print("[ERR!] No input document given, exiting...")
    sys.exit(-1)

if args.output:
    print("Output file: " + args.output)

# Check if the input file exists
if (os.path.exists(args.input) == False):
    print("[ERR!] Input file does not exist, exiting...")
    sys.exit(-2)

# Read the file, then parse it
doc = [line.rstrip('\n') for line in open(args.input)]
parser.parseRandfDoc(doc)

raw_html = gen.generateHtmlHeader("Title of my document")

# Write to pdf
gen.convertHtmlToPdf(raw_html, None)

### End of main program ###


