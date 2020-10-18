from src import styling as sty
from src import generator as gen
from src import cfg

import re

from datetime import date
from itertools import islice

def parseRNoteDoc(doc: [str], style: sty.Styler, raw_html: str) -> str:
    """Parses an input document into an HTML document to later be converted into
    a PDF.

    Parameters
    ----------
    doc
        List of lines from the input document

    style
        Styler object containing style information about the document

    raw_html
        The HTML of the document

    Returns
    -------
    str
        The HTML document that will be turned into a PDF
    """
    cfg.LINE_NO = 0
    doc_iter = iter(doc)

    for l in doc_iter:
        l = l.strip()
        cfg.LINE_NO += 1

        if l.startswith('//') or l == '':
            if cfg.VERBOSE: print('[INFO] Encountered comment or blank line on line {}; skipping'.format(cfg.LINE_NO))
            continue
        elif l.startswith('.pp'):
            if cfg.VERBOSE: print('[INFO] Parsing preprocessor command'.format(cfg.LINE_NO))
            raw_html = parsePpCommand(l, style, raw_html)
        elif l.startswith('$table'):
            if cfg.VERBOSE: print('[INFO] Inserting table beginning on line {}'.format(cfg.LINE_NO))

            # Get table header
            table_header = ' '.join(l.split()[1:]).split(';')
            table_list = []

            # Get table body lines
            for j in islice(doc_iter, 0, None):
                if j.startswith('-'):
                    table_list.append(j)
                elif j ==('$endtable'):
                    cfg.LINE_NO += len(table_list)
                    for k in range(len(table_header)): table_header[k] = formatText(table_header[k])
                    for k in range(len(table_list)): table_list[k] = formatText(table_list[k])
                    raw_html = gen.generateTable(raw_html, table_header, table_list)
                    break
                else: print('[ERR!] Syntax error when processing table, expecting table row or $endtable')
        elif l.startswith('$'):
            if cfg.VERBOSE: print('[INFO] Parsing insert command')
            raw_html = parseInsCommand(l, raw_html)
        elif l.startswith('# '):
            if cfg.VERBOSE: print('[INFO] Parsing level one header')
            raw_html = parseHtmlElement(l, raw_html, '# *', 'h1')
        elif l.startswith('@ '):
            if cfg.VERBOSE: print('[INFO] Parsing level two header')
            raw_html = parseHtmlElement(l, raw_html, '@ *', 'h2')
        elif l.startswith('! '):
            if cfg.VERBOSE: print('[INFO] Parsing level three header')
            raw_html = parseHtmlElement(l, raw_html, '! *', 'h3')
        elif l.startswith('-'):
            # List all bullet points
            if cfg.VERBOSE: print('[INFO] Parsing bullet point list')
            bullet_list = [l]
            for j in islice(doc_iter, 0, None):
                if j.startswith('-'): bullet_list.append(j)
                else: break

            # Process bullet points into document
            cfg.LINE_NO += len(bullet_list)
            for j in range(len(bullet_list)): bullet_list[j] = formatText(bullet_list[j])
            raw_html = gen.generateBulletPoints(raw_html, bullet_list)
        elif l.startswith('= '):
            if cfg.VERBOSE: print('[INFO] Parsing level one header')
            raw_html = parseHtmlElement(l, raw_html, '= *', 'p')
        else: print("[ERR!] Error on or around line {}, could not determine formatting on the following line:\n  >> {}".format(cfg.LINE_NO, l))
    return raw_html


def parsePpCommand(l: str, style: sty.Styler, raw_html: str) -> str:
    """Parses commands that are prefaced with .pp

    Parameters
    ----------
    l
        Command to be parsed
    
    style
        Styler object containing styling information for document

    raw_html
        HTML of the document being created

    Returns
    -------
    str
        The HTML document with new .pp attribute
    """
    # Remove the .pp part of the string, then split it into a list
    l = re.sub('.pp *', '', l)
    cmd = l.split()

    if cmd[0] == 'theme': 
        if cfg.VERBOSE: print('[INFO] Parsing theme preprocessor command')
        style.theme = cmd[1]
    elif cmd[0] == 'margin' or cmd[0] == 'margins':
        if cfg.VERBOSE: print('[INFO] Parsing margin preprocessor command')
        new_margins = cmd[1]
        style.margin = new_margins

        # Set the margins
        if cfg.VERBOSE: print('[INFO] Setting margins to {}'.format(new_margins))
        if new_margins == 'normal': style.topBottom = style.leftRight = 2
        elif new_margins == 'narrow': style.topBottom = style.leftRight = 1
        elif new_margins == 'moderate': style.topBottom, style.leftRight = 1, 0.75
        elif new_margins == 'wide': style.topBottom, style.leftRight = 1, 2
        else:
            print('[ERR!] Error on or around line {}, could not determine margin size, defaulting to normal margins.\n').format(cfg.LINE_NO)
            style.topBottom = style.leftRight = 2
            style.margin = 'normal'
        raw_html = gen.generatePageSize(raw_html, style)
    elif cmd[0] == 'size':
        if cfg.VERBOSE: print('[INFO] Setting new page size')
        new_size = cmd[1].lower()

        # Build list of allowed sizes
        allowed_sizes = ['letter', 'legal', 'elevenseventeen']
        for i in range(7):
            allowed_sizes.append('a{}'.format(i))
            allowed_sizes.append('b{}'.format(i))

        # Check if size is allowed
        if new_size in allowed_sizes:
            if cfg.VERBOSE: print('[INFO] Setting page size to {}'.format(new_size))
            style.pagesize = new_size
        else:
            print('[ERR!] Error on or around line {}, could not determine page size, defaulting to letter (8.5" x 11")\n').format(cfg.LINE_NO)
            style.pagesize = 'letter'
        raw_html = gen.generatePageSize(raw_html, style)
    elif cmd[0] == 'align' or cmd[0] == 'orientation':
        if cfg.VERBOSE: print('[INFO] Setting page orientation')
        new_orient = cmd[1].lower()

        # Set orientation
        if new_orient in ['port', 'portrait', 'vert','verical']: style.orientation = 'portrait'
        elif new_orient in ['land', 'landscape', 'horz', 'horizontal']: style.orientation = 'landscape'
        else:
            print('[ERR!] Error on or around line {}, could not determine page orientation, defaulting to portrait').format(cfg.LINE_NO)
            style.orientation = 'portrait'
        if cfg.VERBOSE: print('[INFO] Setting page orientation to {}'.format(style.orientation))
        raw_html = gen.generatePageSize(raw_html, style)
    elif cmd[0] == 'title':
        if cfg.VERBOSE: print('[INFO] Inserting new document title')
        raw_html = gen.insertDocTitleIntoHtml(raw_html, re.sub('^title?', '', l))
    elif cmd[0] == 'template' or cmd[0] == 'temp' or cmd[0] == 'templ8':
        if cfg.VERBOSE: print('[INFO] Setting document template')
        filename = cmd[1]
        pp_commands = []

        # Read in the new template
        with open('tmplt/' + filename + '.rntp') as f: pp_commands = f.readlines()

        # Process the template
        for cmd in pp_commands: raw_html = parsePpCommand(cmd.strip(), style, raw_html)
    else: print("[ERR!] Error on or around line {}, could not determine preprocessor command '{}'. Skipping this command.".format(cfg.LINE_NO, cmd[0]))
    return raw_html


def parseInsCommand(l: str, raw_html: str) -> str:
    """Parses commands that are prefaced with $

    Parameters
    ----------
    l
        Command to be parsed

    raw_html
        HTML of the document being created

    Returns
    -------
    str
        The HTML document with new $ attribute
    """

    # Remove the $ part of the string, then split it into a list
    l = re.sub('\$', '', l)
    cmd = l.split()
    first = cmd[0]

    if first == 'br' or first == 'hr':
        if cfg.VERBOSE: print('[INFO] Inserting line break')
        raw_html = gen.insertElementIntoHtml(raw_html, '', first)
    elif first == 'date':
        if cfg.VERBOSE: print('[INFO] Inserting date')
        raw_html = gen.insertElementIntoHtml(raw_html, str(date.today()), 'p')
    elif (first == 'wi' or first == 'li') and (len(cmd) >= 2):
        if cfg.VERBOSE: print('[INFO] Inserting image')
        raw_html = gen.insertImageIntoHtml(raw_html, cmd[1])
    else: print("[ERR!] Error on or around line {}, cound not determine insert command '${}'. Skipping this command.".format(cfg.LINE_NO, first))
    return raw_html


def parseHtmlElement(l: str, raw_html: str, pattern: str, element: str) -> str:
    """Parses a HTML element

    Parameters
    ----------
    l
        Line to be parsed

    raw_html
        HTML of the document being created

    pattern
        Regex pattern that is used to search for the element to be added

    element
        HTML element that will be added

    Returns
    -------
    str
        The HTML document with new HTML element
    """
    if cfg.VERBOSE: print('[INFO] Parsing HTML element')
    l = re.sub(pattern, '', l)

    # Format text first
    if cfg.VERBOSE: print('[INFO] Formatting text first')
    l = formatText(l)

    if cfg.VERBOSE: print('[INFO] Inserting new HTML element')
    raw_html = gen.insertElementIntoHtml(raw_html, l, element)
    return raw_html


def formatText(l: str) -> str:
    """ Formats text for styling (bold, italics, etc.)

    Parameters
    ----------
    l
        Line to be formatted

    Returns
    -------
    str
        The formatted line
    """
    l = re.sub('\$date', str(date.today()), l)
    l = l.replace('\*', '&ast;')
    l = l.replace('\_', '&lowbar;')
    l = l.replace('\~', '&tilde;')
    l = textFormatter(l, '***', '<b><i>', '</i></b>')
    l = textFormatter(l, '**', '<b>', '</b>')
    l = textFormatter(l, '*', '<i>', '</i>')
    l = textFormatter(l, '__', '<u>', '</u>')
    l = textFormatter(l, '~~', '<del>', '</del>')
    return l


def textFormatter(text: str, old: str, new1: str, new2: str) -> str:
    """Generic function that formats text

    Parameters
    ----------
    text
        Text to format

    old
        Symbol to look for

    new1
        Opening symbol that will replace

    new2
        Closing symbol that will replace

    Returns
    -------
    str
        The new formatted text
    """
    if text.find(old) != -1 and text.count(old) % 2 == 1:
        text += old
        print('[WARN] Line {} does not have escaped formatter, escaping formatter at end of line'.format(cfg.LINE_NO))
    while text.find(old) != -1:
        text = text.replace(old, new1, 1)
        text = text.replace(old, new2, 1)
    return text
