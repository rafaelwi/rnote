#!/usr/bin/env python3

# RNote Processor
from src import cliargs as cliargs
from src import generator as gen
from src import parser as parser
from src import styling as sty
from src import cfg

import argparse
import sys
import os
import time
from xhtml2pdf import pisa

def run(doc: str, out_file: str):
    # Generate the middle-man HTML, styler object, and parse. Then write to PDF
    doc = doc.split('\r\n')
    raw_html = gen.generateHtmlHeader()
    style = sty.Styler()
    raw_html = parser.parseRNoteDoc(doc, style, raw_html)
    gen.convertHtmlToPdf(raw_html, style, out_file)
