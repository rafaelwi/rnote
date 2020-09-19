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
                doc.asis('@page {{size: {0} {1}; @frame content_frame {{top: {2}cm; bottom: {4}cm; left: {3}cm; right: {5}cm; -pdf-frame-border:1;}}'.format('letter', 'portrait', 2.0, 2.0, 2*2.0, 2*2.0))
                doc.asis('/*EndOf@pageManualStyling*/}')
            with tag('div', id='content'):
                pass
    return ((doc.getvalue()))

def insertElementIntoHtml(html: str, the_text: str, element: str) -> str:
    upper = html.split('</div></body>', 1)[0]
    lower = html.split('</div></body>', 1)[1]
    doc, tag, text, line = Doc().ttl()

    with tag(element):
        text(the_text)
    
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
    print(">" + str(indent_lvl))

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
            text(b)

    # Add in the remaining closing ul tags
    for i in range(indent_lvl):
        doc.asis('</ul>')

    # Add new list to the html and return
    upper = html.split('</div></body>', 1)[0]
    lower = html.split('</div></body>', 1)[1]

    upper += doc.getvalue() + "</div></body>" + lower
    return (upper)

def generateMargins(html: str, topBottom: float, leftRight: float) -> str:
    upper, lower = html.split('/*EndOf@pageManualStyling*/}', 1)[0], html.split('/*EndOf@pageManualStyling*/}', 1)[1]
    doc, tag, text, line = Doc().ttl()

    doc.asis("margin: {0}cm {1}cm {0}cm {1}cm;".format(topBottom, leftRight))
    upper += doc.getvalue() + "/*EndOf@pageManualStyling*/}" + lower
    return (upper)

def generatePageSize(html: str, style: sty.Styler) -> str:
    upper, lower = html.split('/*EndOf@pageManualStyling*/}', 1)[0], html.split('/*EndOf@pageManualStyling*/}', 1)[1]
    doc, tag, text, line = Doc().ttl()

    doc.asis('size: {0} {1}; @frame content_frame {{top: {2}cm; bottom: {4}cm; left: {3}cm; right: {5}cm; -pdf-frame-border:1;}}'.format(style.pagesize, style.orientation, style.topBottom, style.leftRight, 2*style.topBottom, 2*style.leftRight))
    upper = re.sub(r'size:.*;}', doc.getvalue(), upper)

    """
    doc.asis("size: {} {};".format(style.pagesize, style.orientation))
    doc.asis ("@frame {{margin: {0}cm {1}cm {0}cm {1}cm;}}".format(style.topBottom, style.leftRight))
    """
    upper += "/*EndOf@pageManualStyling*/}" + lower
    return (upper)