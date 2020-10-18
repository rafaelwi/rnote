import argparse

def addArgs(p: argparse.ArgumentParser):
    """Adds arguements that will be parsed by the argParser

    Parameters
    ----------
    p: argparse.ArguementParser 
        Object that parses command line arguements
    """
    p.add_argument("-i", "--input", help="name of the input file")
    p.add_argument("-o", "--output", help="name of the output file, default to the name of the input file with a .pdf extension")
    p.add_argument("-d", "--debug", help="turns on debugging features", action='store_true')
    p.add_argument("-v", "--verbose", help="displays verbose information about what the parser is doing", action='store_true')
    p.add_argument("--about", help="displays information about RNote", action='store_true')
