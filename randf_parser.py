import randf_styling as sty
import randf_generator as gen
import re

from datetime import date
from itertools import islice

def parseRandfDoc(doc: list, style: sty.Styler, raw_html: str) -> str:
    line_no = 0
    doc_iter = iter(doc)

    for l in doc_iter:
        line_no += 1
        l = l.strip()

        if l.startswith('//') or l == '':
            print(str(line_no) + ": Encountered a comment or blank line, skipping")
            continue
        elif l.startswith('.pp'):
            raw_html = parsePpCommand(l, line_no, style, raw_html)
        elif l.startswith('$table'):
            print('Inserting table')
            table_header = ' '.join(l.split()[1:]).split(';')
            table_list = []

            for j in islice(doc_iter, 0, None):
                if j.startswith('-'):
                    table_list.append(j)
                elif j ==('$endtable'):
                    line_no += len(table_list)
                    raw_html = gen.generateTable(raw_html, table_header, table_list)
                    break
                else:
                    print('[PARSER_ERR] Syntax error when processing table, expecting table row or $endtable')
        elif l.startswith('$'):
            raw_html = parseInsCommand(l, line_no, raw_html)
        elif l.startswith('# '):
            raw_html = parseHtmlElement(l, line_no, raw_html, '# *', 'h1')
        elif l.startswith('@ '):
            raw_html = parseHtmlElement(l, line_no, raw_html, '@ *', 'h2')
        elif l.startswith('! '):
            raw_html = parseHtmlElement(l, line_no, raw_html, '! *', 'h3')
        elif l.startswith('-'):
            # Create a new list with all of the lines with bullets, and then
            # parse them later. Start with current point.
            bullet_list = [l]

            for j in islice(doc_iter, 0, None):
                if j.startswith('-'):
                    bullet_list.append(j)
                else:
                    break

            # Process this into meaningful document :)
            line_no += len(bullet_list)
            raw_html = gen.generateBulletPoints(raw_html, bullet_list)
        elif l.startswith('= '):
            raw_html = parseHtmlElement(l, line_no, raw_html, '= *', 'p')
        else:
            print("[PARSER_ERR] Error on or around line {}, could not determine formatting on the following line:\n  >> {}".format(line_no, l))
    return raw_html


def parsePpCommand(l: str, line_no: int, style: sty.Styler, raw_html: str) -> str:
    # Remove the .pp part of the string, then split it into a list
    l = re.sub('.pp *', '', l)
    cmd = l.split()

    if cmd[0] == 'theme':
        style.theme = cmd[1]
    elif cmd[0] == 'margin' or cmd[0] == 'margins':
        new_margins = cmd[1]
        style.margin = new_margins

        # Set the margins
        print('Setting margins to {}'.format(new_margins))
        if new_margins == 'normal':
            style.topBottom = style.leftRight = 2
        elif new_margins == 'narrow':
            style.topBottom = style.leftRight = 1
        elif new_margins == 'moderate':
            style.topBottom, style.leftRight = 1, 0.75
        elif new_margins == 'wide':
            style.topBottom, style.leftRight = 1, 2
        else:
            print('[PARSER_ERR] Error on or around line {}, could not determine margin size, defaulting to normal margins.\n').format(line_no)
            style.topBottom = style.leftRight = 2
            style.margin = 'normal'
        raw_html = gen.generatePageSize(raw_html, style)
    elif cmd[0] == 'size':
        new_size = cmd[1].lower()

        # Build list of allowed sizes
        allowed_sizes = ['letter', 'legal', 'elevenseventeen']
        for i in range(7):
            allowed_sizes.append('a{}'.format(i))
            allowed_sizes.append('b{}'.format(i))

        # Check if size is allowed
        if new_size in allowed_sizes:
            style.pagesize = new_size
        else:
            print('[PARSER_ERR] Error on or around line {}, could not determine page size, defaulting to letter (8.5" x 11")\n').format(line_no)
            style.pagesize = 'letter'
        raw_html = gen.generatePageSize(raw_html, style)
    elif cmd[0] == 'align' or cmd[0] == 'orientation':
        print('Setting orientation')
        new_orient = cmd[1].lower()

        # Set orientation
        if new_orient in ['port', 'portrait', 'vert','verical']:
            style.orientation = 'portrait'
        elif new_orient in ['land', 'landscape', 'horz', 'horizontal']:
            style.orientation = 'landscape'
        else:
            print('[PARSER_ERR] Error on or around line {}, could not determine page orientation, defaulting to portrait').format(line_no)
            style.orientation = 'portrait'
        raw_html = gen.generatePageSize(raw_html, style)
    elif cmd[0] == 'title':
        raw_html = gen.insertDocTitleIntoHtml(raw_html, re.sub('^title?', '', l))
    elif cmd[0] == 'template' or cmd[0] == 'temp' or cmd[0] == 'templ8':
        print('Setting template')
        filename = cmd[1]
        pp_commands = []
        with open('templates/' + filename + '.rdtp') as f:
            pp_commands = f.readlines()

        for cmd in pp_commands:
            raw_html = parsePpCommand(cmd.strip(), line_no, style, raw_html)
    else:
        print("[PARSER_ERR] Error on or around line {}, could not determine preprocessor command '{}'. Skipping this command.".format(line_no, cmd[0]))
    return raw_html


def parseInsCommand(l: str, line_no: int, raw_html: str) -> str:
    # Remove the $ part of the string, then split it into a list
    l = re.sub('\$', '', l)
    cmd = l.split()
    first = cmd[0]

    if first == 'br' or first == 'hr':
        print('line break')
        raw_html = gen.insertElementIntoHtml(raw_html, '', first)
    elif first == 'date':
        raw_html = gen.insertElementIntoHtml(raw_html, str(date.today()), 'p')
    elif (first == 'wi' or first == 'li') and (len(cmd) >= 2):
        raw_html = gen.insertImageIntoHtml(raw_html, cmd[1])
    else:
        print("[PARSER_ERR] Error on or around line {}, cound not determine insert command '${}'. Skipping this command.".format(line_no, first))
    return raw_html


def parseHtmlElement(l: str, line_no: int, raw_html: str, pattern: str, element: str) -> str:
    l = re.sub(pattern, '', l)

    # Before adding the line, see if there is anything that needs to be parsed
    # by the insert command
    l = re.sub('\$date', str(date.today()), l)
    l = l.replace('\*', '&ast;')
    l = l.replace('\_', '&lowbar;')
    l = l.replace('\~', '&tilde;')
    l = textFormatter(l, '***', '<b><i>', '</i></b>')
    l = textFormatter(l, '**', '<b>', '</b>')
    l = textFormatter(l, '*', '<i>', '</i>')
    l = textFormatter(l, '__', '<u>', '</u>')
    l = textFormatter(l, '~~', '<del>', '</del>')
    raw_html = gen.insertElementIntoHtml(raw_html, l, element)
    return raw_html


def textFormatter(text: str, old: str, new1: str, new2: str) -> str:
    if text.find(old) != -1 and text.count(old) % 2 == 1:
        text += old
        print('WARNING: Current line does not have escaped formatter, escaping formatter at end of line')
    while text.find(old) != -1:
        text = text.replace(old, new1, 1)
        text = text.replace(old, new2, 1)
    return text
