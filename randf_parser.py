import randf_styling as sty
import re

def parseRandfDoc(doc: list, style: sty.Styler):
    line_no = 0

    for l in doc:
        line_no += 1
        l = l.strip()

        if l.startswith('//') or l == '':
            print("Encountered a comment or blank line, skipping")
            continue
        if l.startswith('.pp'):
            parsePpCommand(l, line_no, style)
        elif l.startswith('$'):
            parseInsCommand(l, line_no)
        elif l.startswith('# '):
            print("parsing title")
        elif l.startswith('@ '):
            print("parsing bytag")
        elif l.startswith('! '):
            print("parsing header")
        elif l.startswith('- '):
            print("parsing bullet")
        elif l.startswith('= '):
            print("parsing paragraph")  
        else:
            print("[PARSER_ERR] Error on or around line {}, could not determine formatting on the following line:\n  >> {}".format(line_no, l))
        

def parsePpCommand(l: str, line_no: int, style: sty.Styler):
    # Remove the .pp part of the string, then split it into a list
    l = re.sub('.pp *', '', l)
    cmd = l.split()

    if cmd[0] == 'theme':
        print('setting theme')
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
        print('set title')
    elif cmd[0] == 'template' or cmd[0] == 'temp' or cmd[0] == 'templ8':
        print('set template')
    else:
        print("[PARSER_ERR] Error on or around line {}, could not determine preprocessor command '{}'. Skipping this command.".format(line_no, cmd[0]))
        return

def parseInsCommand(l: str, line_no: int):
    # Remove the $ part of the string, then split it into  a list
    l = re.sub('\$', '', l)
    cmd = l.split()
    first = cmd[0]

    if first == 'br':
        print('line break')
    elif first == 'date':
        print('date')
    elif first == 'wi':
        print('web image')
    elif first == 'li':
        print('local image')
    elif first == 'table':
        print('table')
    else:
        print("[PARSER_ERR] Error on or around line {}, cound not determine insert command '${}'. Skipping this command.".format(line_no, first))
