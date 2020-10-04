import randf_styling as sty

import re

from yattag import Doc, indent
from xhtml2pdf import pisa
from datetime import datetime

def generateHtmlHeader() -> str:
    doc, tag, text, line = Doc().ttl()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            doc.stag('meta', charset='utf-8')
            with tag('title'):
                text('')
            doc.stag('meta', name='description', content='An HTML file generated by the RANDF compiler.')
            doc.stag('meta', name='author', content='RANDF Compiler')
        with tag('body'):
            with tag('style'):
                style = sty.Styler() # Temp obj.
                doc.asis('@page {{size: {} {}; @frame {{top: {}cm; left: {}cm; height: {}cm; width: {}cm; -pdf-frame-border:1;}}'.format(style.pagesize, style.orientation, style.top, style.left, style.height, style.width))
                doc.asis('/*EndOf@pageManualStyling*/}')
                del style
            with tag('div', id='content'):
                pass
    return ((doc.getvalue()))

def insertElementIntoHtml(html: str, the_text: str, element: str) -> str:
    upper = html.split('</div></body>', 1)[0]
    lower = html.split('</div></body>', 1)[1]
    doc, tag, text, line = Doc().ttl()

    with tag(element):
        doc.asis(formatText(the_text))
    
    upper += doc.getvalue() + "</div></body>" + lower
    return (upper)

def insertDocTitleIntoHtml(html: str, the_title: str) -> str:
    upper = html.split('</title>', 1)[0]
    lower = html.split('</title>', 1)[1]
    upper += the_title + '</title>' + lower
    return (upper)

def insertImageIntoHtml(html: str, img: str) -> str:
    upper = html.split('</div></body>', 1)[0]
    lower = html.split('</div></body>', 1)[1]
    doc, tag, text, line = Doc().ttl()

    doc.stag('img', src=img)

    upper += doc.getvalue() + '</div></body>' + lower
    return (upper)


def convertHtmlToPdf(raw_html: str, style: sty.Styler, out_file: str) -> bool:
    result_file = open(out_file, "w+b")
    status = pisa.CreatePDF(raw_html, dest=result_file, default_css=style.theme, debug=1)
    #status = pisa.CreatePDF(raw_html, dest=result_file, debug=1)
    result_file.close()
    return status

def generateBulletPoints(html: str, bullets: list):
    first_line = bullets[0]

    # Count the number of dashes in the first one
    indent_lvl = first_line.split()[0].count('-')

    # Create the yattag stuff
    doc, tag, text, line = Doc().ttl()

    # Create the level of indent that we need for the first line
    for i in range(indent_lvl):
        doc.asis('<ul>')

    for b in bullets:
        # Count the level of indent that we are currently on and compare
        current_indent_lvl = b.split()[0].count('-')

        # If there are more bullets, add the difference number of ul tags
        if current_indent_lvl > indent_lvl:
            for i in range(current_indent_lvl - indent_lvl):
                doc.asis('<ul>')
            indent_lvl = current_indent_lvl

        # If there are fewer bullets, add the difference of ending ul tags
        elif current_indent_lvl < indent_lvl:
            for i in range(indent_lvl - current_indent_lvl):
                doc.asis('</ul>')
            indent_lvl = current_indent_lvl

        # Add the li tag
        with tag('li'):
            b = re.sub('^(-+)', '', b)
            b = b.strip()
            doc.asis(formatText(b))

    # Add in the remaining closing ul tags
    for i in range(indent_lvl):
        doc.asis('</ul>')

    # Add new list to the html and return
    upper = html.split('</div></body>', 1)[0]
    lower = html.split('</div></body>', 1)[1]

    upper += doc.getvalue() + "</div></body>" + lower
    return (upper)


def generatePageSize(html: str, style: sty.Styler) -> str:
    upper, lower = html.split('/*EndOf@pageManualStyling*/}', 1)[0], html.split('/*EndOf@pageManualStyling*/}', 1)[1]
    doc, tag, text, line = Doc().ttl()
    style.width = 1
    style.height = 1

    doc.asis('size: {} {}; @frame {{top: {}cm; left: {}cm; height: {}cm; width: {}cm;}}'.format(style.pagesize, style.orientation, style.top, style.left, style.height, style.width))
    upper = re.sub(r'size:.*;}', doc.getvalue(), upper)

    upper += "/*EndOf@pageManualStyling*/}" + lower
    return upper

def generateTable(html: str, head: [str], rows: [str]) -> str:
    print(head)
    print(rows)

    upper, lower = html.split('</div></body>', 1)[0], html.split('</div></body>', 1)[1]
    doc, tag, text, line = Doc().ttl()

    with tag('table'):
        # Generate header
        with tag('tr'):
            for i in head:
                with tag('th'):
                    doc.asis(formatText(i.strip()))
        
        # Generate content in table
        for r in rows:
            with tag('tr'):
                r = r.split(';')
                with tag('td'):
                    doc.asis(formatText(r[0][2:]))
                for s in r[1:]:
                    with tag('td'):
                        doc.asis(formatText(s.strip()))

    # Insert table into doc
    upper += doc.getvalue() + '</div></body>' + lower
    return indent(upper)

def formatText(text: str) -> str:
    # TODO: Text formatting for table data, headers, inserts, etc.

    # Look for escaped text
    text = text.replace('\*', '&ast;')
    text = text.replace('\_', '&lowbar;')
    text = text.replace('\~', '&tilde;')

    # Look for bolded and italicized text (***)
    text = textFormatter(text, '***', '<b><i>', '</i></b>')

    # Look for bolded text (**)
    text = textFormatter(text, '**', '<b>', '</b>')

    # Look for italicized text (*)
    text = textFormatter(text, '*', '<i>', '</i>')

    # Look for underlined text (__)
    text = textFormatter(text, '__', '<u>', '</u>')

    # Look for strikethrough text
    text = textFormatter(text, '~~', '<del>', '</del>')
    return text

def textFormatter(text: str, old: str, new1: str, new2: str) -> str:
    if text.find(old) != -1 and text.count(old) % 2 == 1:
        text += old
        print('WARNING: Current line does not have escaped formatter, escaping formatter at end of line')
    while text.find(old) != -1:
        text = text.replace(old, new1, 1)
        text = text.replace(old, new2, 1)
    return text
