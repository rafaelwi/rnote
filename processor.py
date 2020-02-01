# RANDF Processor: Takes a raw file and converts it to a compiled document.

import randf_cliargs as cliargs
import randf_generator as gen
import randf_parser as parser
import randf_styling as sty

import argparse
import sys
import os
import time
from xhtml2pdf import pisa

### Main Program ###
start_time = time.time()
arg_parser = argparse.ArgumentParser()
cliargs.addArgs(arg_parser)
args = arg_parser.parse_args()
out_file = 'out.pdf'

# Get the cl args
if args.input:
    print("Input file: " + args.input)
else:
    print("[ERR!] No input document given, exiting...")
    sys.exit(-1)

if args.output:
    print("Output file: " + args.output)
    out_file = args.output
else:
    print("[WARN] No output document given, defaulting to 'out.pdf'")

# Check if the input file exists
if (os.path.exists(args.input) == False):
    print("[ERR!] Input file does not exist, exiting...")
    sys.exit(-2)

# Generate the middle-man HTML file that will be converted to PDF
raw_html = gen.generateHtmlHeader()

# Read the file, then parse it
doc = [line.rstrip('\n') for line in open(args.input)]
style = sty.Styler()
raw_html = parser.parseRandfDoc(doc, style, raw_html)

# Write the html to a temp file
f = open("a.html", "w")
f.write(raw_html)
f.close()

# Write to PDF
gen.convertHtmlToPdf(raw_html, style, out_file)
print("[RANDF] File {} successfully converted to PDF {}".format(args.input, out_file))
print("[RANDF] Process took {:.4f} seconds".format(time.time() - start_time))
### End of main program ###
