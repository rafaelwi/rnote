import tinycss
import os

class Styler:
    def __init__(self):
        self.theme = 'light'
        self.margin = 'normal'
        self.topBottom = 2.0
        self.leftRight = 2.0
        self.pagesize = 'letter'
        self.orientation = 'portrait'
        self.pgnum = False
        self.title = 'New Document'
        self.template = ''

    @property
    def theme(self):
        return self._theme
    
    @theme.setter
    def theme(self, theme_fn):
        """ Sets a new theme for the document """
        # Check if the file passed in exists
        filename = "themes/" + theme_fn + ".css"
        if (os.path.exists(filename) == False):
            print("[PARSER_ERR] Could not find theme file '{}'. Please make sure that the theme is in the theme/ folder. Falling back on default theme.".format(filename))
            return

        # Open and read the new themesheet from the themes/ folder
        f = open(filename, "r")
        new_theme = f.read()
        f.close()

        # Validate the CSS for the document and set the CSS if it is valid
        verifier = tinycss.make_parser('page3')
        parsed_contents = verifier.parse_stylesheet(new_theme)
        self._theme = new_theme

        """
        if parsed_contents.errors == []:
            self._theme = new_theme
        else:
            print('[PARSER_ERR] {} errors were encountered when attempting to parse the stylesheet. The following errors are:'.format(len(parsed_contents.errors)))
            for i in parsed_contents.errors:
                print("  {}".format(i))
        """                

    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, new_margin):
        """ Sets a new margin """
        self._margin = new_margin

    @property
    def topBottom(self):
        return self._topBottom

    @topBottom.setter
    def topBottom(self, new_TB):
        """ Sets new topBottom value """
        self._topBottom = new_TB

    @property
    def leftRight(self):
        return self._leftRight

    @leftRight.setter
    def leftRight(self, new_LR):
        """ Sets new leftRight value """
        self._leftRight = new_LR

    @property
    def pagesize(self):
        return self._pagesize

    @pagesize.setter
    def pagesize(self, new_pagesize):
        """ Sets a new pagesize """
        self._pagesize = new_pagesize

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, new_orientation):
        """ Sets a new orientation for the document """
        self._orientation = new_orientation

    @property
    def pgnum(self):
        return self._pgnum
    
    @pgnum.setter
    def pgnum(self, onOrOff: bool):
        """ Turns the page numbers on or off """
        self._pgnum = onOrOff

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        """ Sets the title of the document """
        self._title = new_title

    @property
    def template(self):
        return self._template

    @template.setter
    def template(self, new_template):
        """ Sets the preprocessor command template of the document """
        self._template = new_template
