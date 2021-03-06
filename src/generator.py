from src import styling as sty
from src import cfg

import re

from yattag import Doc, indent
from xhtml2pdf import pisa
from datetime import datetime

def generateHtmlHeader() -> str:
    """Generates the skeleton HTML file

    Returns
    -------
    str
        A string containing the contents of the HTML file generated
    """
    doc, tag, text, line = Doc().ttl()
    doc.asis('<!DOCTYPE html>')
    
    with tag('html'):
        if cfg.VERBOSE: print('[INFO] Generating HTML header')
        with tag('head'):
            doc.stag('meta', charset='utf-8')
            with tag('title'): text('')
            doc.stag('meta', name='description', content='An HTML file generated by the RNote compiler.')
            doc.stag('meta', name='author', content='RNote Compiler')
        if cfg.VERBOSE: print('[INFO] Generating HTML body')
        with tag('body'):
            with tag('style'):
                style = sty.Styler() # Temp obj.
                doc.asis('@page {{size: {} {}; @frame {{top: {}cm; left: {}cm; height: {}cm; width: {}cm; -pdf-frame-border:1;}}'.format(style.pagesize, style.orientation, style.top, style.left, style.height, style.width))
                doc.asis('/*EndOf@pageManualStyling*/}')
                del style
            with tag('div', id='content'): pass
    return doc.getvalue()


def insertElementIntoHtml(html: str, the_text: str, element: str) -> str:
    """Inserts a simple HTML element into the document

    Parameters
    ----------
    html
        The HTML file that will get the new element
    the_text
        Text value of the new element
    element
        New HTML element to insert

    Returns
    -------
    str
        The HTML document with new element inserted
    """
    doc, tag, text, line = Doc().ttl()
    with tag(element):
        if cfg.VERBOSE: print('[INFO] Inserting {} element'.format(element))
        doc.asis(the_text)
    upper, lower = html.split('</div></body>', 1)[0], html.split('</div></body>', 1)[1]
    return upper + doc.getvalue() + "</div></body>" + lower


def insertDocTitleIntoHtml(html: str, the_title: str) -> str:
    """Sets the title of the document

    Parameters
    ---------
    html
        The document that will get the new title

    the_title
        New title for the document

    Returns
    -------
    str
        The HTML document with the new document title
    """
    upper, lower = html.split('</title>', 1)[0], html.split('</title>', 1)[1]
    if cfg.VERBOSE: print('[INFO] Setting new document title')
    return upper + the_title + '</title>' + lower


def insertImageIntoHtml(html: str, img: str) -> str:
    """Inserts an image into the document. Despite being labeled differently,
    $wi and $li use the same function.

    Parameters
    ----------
    html
        The document that will get the new image

    img
        Path or URL to the new image

    Returns
    -------
    str
        The HTML document with the new image
    """
    doc, tag, text, line = Doc().ttl()
    doc.stag('img', src=img)
    upper, lower = html.split('</div></body>', 1)[0], html.split('</div></body>', 1)[1]
    if cfg.VERBOSE: print('[INFO] Adding image')
    return upper + doc.getvalue() + '</div></body>' + lower


def convertHtmlToPdf(raw_html: str, style: sty.Styler, out_file: str) -> bool:
    """Converts HTML middle-man document into beautiful PDF

    Parameters
    ----------
    raw_html
        The HTML of the document to be converted
    
    style
        Styler object that contains CSS rules for the HTML document

    out_file
        Path to the new PDF document

    Returns
    -------
    bool
        True if conversion was successful, False otherwise
    """
    result_file = open(out_file, "w+b")
    status = pisa.CreatePDF(raw_html, dest=result_file, default_css=style.theme, debug=1)
    result_file.close()
    return status


def generateBulletPoints(html: str, bullets: list) -> str:
    """Generates bullet point list for a document

    Parameters
    ----------
    html
        The HTML document to get the new bullet list
    
    bullets
        List of lines that contain the bullets

    Returns
    -------
    str
        The HTML document with new bullet list

    """
    doc, tag, text, line = Doc().ttl()
    first_line = bullets[0]

    # Count the indent level and set it for the first line
    original_indent_lvl = first_line.split()[0].count('-')
    doc.asis('<ul>' * original_indent_lvl)

    for b in bullets:
        # Count the level of indent that we are currently on and compare
        current_indent_lvl = b.split()[0].count('-')

        # If there are more bullets, add the difference number of ul tags
        if current_indent_lvl > original_indent_lvl:
            if cfg.VERBOSE: print('[INFO] Increasing indent level of list')
            doc.asis('<ul>' * (current_indent_lvl - original_indent_lvl))
            original_indent_lvl = current_indent_lvl

        # If there are fewer bullets, add the difference of ending ul tags
        elif current_indent_lvl < original_indent_lvl:
            if cfg.VERBOSE: print('[INFO] Decreasing indent level of list')
            doc.asis('</ul>' * (original_indent_lvl - current_indent_lvl))
            original_indent_lvl = current_indent_lvl

        # Add the li tag
        with tag('li'):
            b = re.sub('^(-+)', '', b)
            b = b.strip()
            doc.asis(b)

    # Add in the remaining closing ul tags and add the list to the HTML
    doc.asis('</ul>' * original_indent_lvl)
    if cfg.VERBOSE: print('[INFO] Adding list')
    upper, lower = html.split('</div></body>', 1)[0], html.split('</div></body>', 1)[1]
    return upper + doc.getvalue() + "</div></body>" + lower


def generatePageSize(html: str, style: sty.Styler) -> str:
    """Sets the page size of the document

    Parameters
    ----------
    html
        The HTML document that will have its page size changed

    style
        Styler object that contains new page size information

    Returns
    -------
    str
        The HTML document with the new page size
    """
    doc, tag, text, line = Doc().ttl()
    style.width, style.height = 1, 1
    upper, lower = html.split('/*EndOf@pageManualStyling*/}', 1)[0], html.split('/*EndOf@pageManualStyling*/}', 1)[1]
    doc.asis('size: {} {}; @frame {{top: {}cm; left: {}cm; height: {}cm; width: {}cm;}}'.format(style.pagesize, style.orientation, style.top, style.left, style.height, style.width))
    upper = re.sub(r'size:.*;}', doc.getvalue(), upper)
    if cfg.VERBOSE: print('[INFO] Setting page size to {}'.format(style.pagesize))
    return upper + "/*EndOf@pageManualStyling*/}" + lower


def generateTable(html: str, head: [str], rows: [str]) -> str:
    """Generates a table to insert into the document

    Parameters
    ----------
    html
        HTML document that will get the new table

    head
        Header row of the new table

    rows
        Body rows of the new table

    Returns
    -------
    str
        The HTML document with the new table
    """
    doc, tag, text, line = Doc().ttl()

    # Generate table header
    with tag('table'):
        if cfg.VERBOSE: print('[INFO] Generating table header')
        with tag('tr'):
            for i in head: 
                with tag('th'): 
                    doc.asis(i.strip())
        
        # Generate content in table
        if cfg.VERBOSE: print('[INFO] Generating table rows')
        for r in rows:
            with tag('tr'):
                r = r.split(';')
                with tag('td'): doc.asis(r[0][2:])
                for s in r[1:]:
                    with tag('td'):
                        doc.asis(s.strip())

    # Insert table into doc
    if cfg.VERBOSE: print('[INFO] Inserting table')
    upper, lower = html.split('</div></body>', 1)[0], html.split('</div></body>', 1)[1]
    return upper + doc.getvalue() + '</div></body>' + lower
