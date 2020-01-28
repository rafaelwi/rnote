# Rafael's Notetaking Document Format Specifications
This document is intended to explain the syntax of RANDF files. There are three
types of syntax: preprocessor commands, insert commands, and styling commands. 
Preprocessor commands set the overall styling and appearance of the document. 
All preprocessor commands are prefaced with `.pp`. Insert commands insert 
styling elements into the document. All insert commands are prefaced with `$`. 
Styling commands modify the appearance of the lines of the docuemnt. They are 
prefaced with various symbols.

## Preprocessor Commands
All preprocssor commands are prefaced with `.pp`

`theme ThemeName`<br>
Sets the font and colors of the document. Users can choose between a predefined 
theme, or can create their own and place it in the `themes/` folder.

**Options**<br>
light [DEFAULT] - A default light theme, white background with black text.<br>
dark - A dark document theme, black background with white text.<br>
USERDEFINED - A user-defined theme. Must be placed in the `themes/` folder, and
called with the theme name.

<hr>

`margin MarginSize`<br>
Sets the margins of the compiled docuemnt. Margin names are based on those 
from a popular word processor.

**Options**<br>
normal [DEFAULT] - 1" margins on all sides of the document page<br>
narrow - 0.5" margins on all sizes of the document page<br>
moderate - 1" margins on the top and bottom, 0.75" margins on the left and 
right of the document page<br>
wide - 1" marigns on the top and bottom, 2" margins on the left and right of 
the document

<hr>

`size PageSize`<br>
Sets the size of the document page.

**Options**<br>
letter [DEFAULT] - 8.5" x 11" sized pages<br>
legal - 8.5" x 14" sized pages<br>
A4 / a4 - 210mm x 297mm sized pages

<hr>

`align Orientation  / orientation Orientation`<br>
Sets the page orientation.

**Options**<br>
port / portrait / vert / verical [DEFAULT] - Orients the pages in a vertical manner<br>
land / landscape / horz / horizontal - Orients the pages in a horizontal manner <br>

<hr>

`pgnum OnOrOff / pagenum OnOrOff`<br>
Sets whether page numbers are on or off.

**Options**<br>
off [DEFAULT] - No page numbering<br>
on - Pages are numbered

<hr>

`title DocumentTitle`<br>
Sets the title of the document when compiled to PDF.

<hr>

`template TemplateName / temp TemplateName / templ8 TemplateName`<br>
Uses a template file found in the `template/` folder to determine preprocessor commands.

<hr>

## Styling Commands
These commands style text in the document.

| Command | Action | Example |
|---|---|---|
| # | Creates a title for the document. | `# My First Document` |
| @ | Creates a secondary header for the document. Great for bylines and dates | `@ By Rafael Wiska Ilnicki \| $date`
| ! | Creates a section header | `! Chapter 1` |
| - | Creates a bullet point. Adding more increases the level of indentation. | `- This is a point`<br>`-- This is an indented point`
| = | Creates a paragraph of text with no indentation. | `= This is a paragraph of text. Not a bullet point, this would not be indented when compiled.`|
| \*text\* | Italicizes text. | \*This text is italiciz*ed\* |
| \*\*text\*\* | Bolds text. | \*\*This text is bolded\*\* |
| \_\_text\_\_ | Underlines text. | \_\_This text is underlined\_\_ |

<hr>

## Insert Commands
These commands insert styling into the final document.

| Command | Action |
|---|---|
| $br | Line break |
| $hr | Horizontal rule |
| $date | Inserts the current date |
| $wi *URL* | Inserts an image found on the web from the given URL |
| $li *FILENAME* | Inserts an image found at the given filepath |

<hr>

## Table Formatting
To insert a table into a RANDF document, use the following syntax:
- To define the header of the table, use `$table Header Item 1; Header Item 2; ...`
- To add an item to the table, use `- Item 1 Col A; Item 1 Col B; ...`
- To end a table, use `$endtable`

**Syntax Example**
```
$table Name; ID; Favourite Colour
- Rafael; 1234; Blue
- Bob; 1235; Red
- Nigel; 6543; Purple
- Tina; 2112; Yellow
$endtable
```

**Output**
| Name | ID | Favourite Colour |
|---|---|---|
Rafael | 1234 | Blue
Bob | 1235 | Red
Nigel | 6543 | Purple
Tina | 2112 | Yellow
