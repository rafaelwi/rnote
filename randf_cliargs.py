import argparse

def addArgs(p: argparse.ArgumentParser):
    p.add_argument("-i", "--input", help="name of the input file")
    p.add_argument("-o", "--output", help="name of the output file, default to the name of the input file with a .pdf extension")
