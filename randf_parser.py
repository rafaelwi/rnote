import randf_styling as sty
import randf_generator as gen
import re

from datetime import date

def parseRandfDoc(doc: list, style: sty.Styler, raw_html: str) -> str:
    line_no = 0

    for l in doc:
        line_no += 1
        l = l.strip()

        if l.startswith('//') or l == '':
            print("Encountered a comment or blank line, skipping")
            continue
        if l.startswith('.pp'):
            raw_html = parsePpCommand(l, line_no, style, raw_html)
        elif l.startswith('$'):
            raw_html = parseInsCommand(l, line_no, raw_html)
        elif l.startswith('# '):
            raw_html = parseHtmlElement(l, line_no, raw_html, '# *', 'h1')
        elif l.startswith('@ '):
            raw_html = parseHtmlElement(l, line_no, raw_html, '@ *', 'h2')
        elif l.startswith('! '):
            raw_html = parseHtmlElement(l, line_no, raw_html, '! *', 'h3')
        elif l.startswith('- '):
            print("parsing bullet")
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
    elif cmd[0] == 'margin':
        print('set margin')
    elif cmd[0] == 'size':
        print('set size')
    elif cmd[0] == 'align' or cmd[0] == 'orientation':
        print('set align')
    elif cmd[0] == 'pgnum':
        print('set pgnum')
    elif cmd[0] == 'title':
        raw_html = gen.insertDocTitleIntoHtml(raw_html, re.sub('^title?', '', l))
    elif cmd[0] == 'template' or cmd[0] == 'temp' or cmd[0] == 'templ8':
        print('set template')
    else:
        print("[PARSER_ERR] Error on or around line {}, could not determine preprocessor command '{}'. Skipping this command.".format(line_no, cmd[0]))
    
    return raw_html

def parseInsCommand(l: str, line_no: int, raw_html: str) -> str:
    # Remove the $ part of the string, then split it into  a list
    l = re.sub('\$', '', l)
    cmd = l.split()
    first = cmd[0]

    if first == 'br':
        print('line break')
        raw_html = gen.insertElementIntoHtml(raw_html, '', 'br')
    elif first == 'date':
        raw_html = gen.insertElementIntoHtml(raw_html, str(date.today()), 'p')
    elif (first == 'wi' or first == 'li') and (len(cmd) >= 2):
        print('web image')
        raw_html = gen.insertImageIntoHtml(raw_html, cmd[1])
    elif first == 'table':
        print('table')
    else:
        print("[PARSER_ERR] Error on or around line {}, cound not determine insert command '${}'. Skipping this command.".format(line_no, first))
    
    return raw_html

def parseHtmlElement(l: str, line_no: int, raw_html: str, pattern: str, 
    element: str) -> str:
    l = re.sub(pattern, '', l)

    # Before adding the line, see if there is anything that needs to be parsed
    # by the insert command thing
    l = re.sub('\$date', str(date.today()), l)

    raw_html = gen.insertElementIntoHtml(raw_html, l, element)
    return raw_html

