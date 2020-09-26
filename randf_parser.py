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
        elif l.startswith('$'):
            raw_html = parseInsCommand(l, line_no, raw_html)
        elif l.startswith('# '):
            raw_html = parseHtmlElement(l, line_no, raw_html, '# *', 'h1')
        elif l.startswith('@ '):
            raw_html = parseHtmlElement(l, line_no, raw_html, '@ *', 'h2')
        elif l.startswith('! '):
            raw_html = parseHtmlElement(l, line_no, raw_html, '! *', 'h3')
        elif l.startswith('-'):
            """ Create a new list with all of the lines with bullets, and then
                parse them later """
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
        # Determine the margin size
        new_margins = cmd[1]
        style.margin = new_margins
        print('Setting margins to {}'.format(new_margins))
        if new_margins == 'normal':
            style.topBottom = style.leftRight = 2
            raw_html = gen.generatePageSize(raw_html, style)
        elif new_margins == 'narrow':
            style.topBottom = style.leftRight = 1
            raw_html = gen.generatePageSize(raw_html, style)
        elif new_margins == 'moderate':
            style.topBottom, style.leftRight = 1, 0.75
            raw_html = gen.generatePageSize(raw_html, style)
        elif new_margins == 'wide':
            style.topBottom, style.leftRight = 1, 2
            raw_html = gen.generatePageSize(raw_html, style)
        else:
            print('[PARSER_ERR] Error on or around line {}, could not determine margin size, defaulting to normal margins.\n').format(line_no)
            style.margin = 'normal'
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
            raw_html = gen.generatePageSize(raw_html, style)
        else:
            print('[PARSER_ERR] Error on or around line {}, could not determine page size, defaulting to letter (8.5" x 11")\n').format(line_no)
            style.pagesize = 'letter'
    elif cmd[0] == 'align' or cmd[0] == 'orientation':
        print('Setting orientation')
        new_orient = cmd[1].lower()

        # Set orientation
        if new_orient in ['port', 'portrait', 'vert','verical']:
            style.orientation = 'portrait'
            raw_html = gen.generatePageSize(raw_html, style)
        elif new_orient in ['land', 'landscape', 'horz', 'horizontal']:
            style.orientation = 'landscape'
            raw_html = gen.generatePageSize(raw_html, style)
        else:
            print('[PARSER_ERR] Error on or around line {}, could not determine page orientation, defaulting to portrait').format(line_no)
            style.orientation = 'portrait'
    elif cmd[0] == 'pgnum':
        # TODO: PAGE NUMBERS
        print("Feature '.pp pgnum' has not been implemented yet!")
    elif cmd[0] == 'title':
        raw_html = gen.insertDocTitleIntoHtml(raw_html, re.sub('^title?', '', l))
    elif cmd[0] == 'template' or cmd[0] == 'temp' or cmd[0] == 'templ8':
        print('Setting template')
        filename = cmd[1]
        pp_commands = []
        with open('templates/' + filename + '.rdtp') as f:
            pp_commands = f.readlines()
            #NOTE: It may be more efficient to read one line in at a time and do its instruction
        
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

    if first == 'br':
        print('line break')
        raw_html = gen.insertElementIntoHtml(raw_html, '', 'br')
    elif first == 'hr':
        raw_html = gen.insertElementIntoHtml(raw_html, '', 'hr')
    elif first == 'date':
        raw_html = gen.insertElementIntoHtml(raw_html, str(date.today()), 'p')
    elif (first == 'wi' or first == 'li') and (len(cmd) >= 2):
        raw_html = gen.insertImageIntoHtml(raw_html, cmd[1])
    elif first == 'table':
        print('TODO: table')
    else:
        print("[PARSER_ERR] Error on or around line {}, cound not determine insert command '${}'. Skipping this command.".format(line_no, first))
    return raw_html

def parseHtmlElement(l: str, line_no: int, raw_html: str, pattern: str, element: str) -> str:
    l = re.sub(pattern, '', l)

    # Before adding the line, see if there is anything that needs to be parsed
    # by the insert command thing
    l = re.sub('\$date', str(date.today()), l)

    raw_html = gen.insertElementIntoHtml(raw_html, l, element)
    return raw_html

