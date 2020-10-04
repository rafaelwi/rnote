class PageDimensions:
    def __init__(self, w: int, h: int):
        self.width = w
        self.height = h
    
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, wi):
        self._width = wi
    
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, hi):
        self._height = hi
