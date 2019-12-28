class FloatRect(object):
    def __init__(self, left, top, width, height):
        self._left = left
        self._top = top
        self._width = width
        self._height = height
        pass

    def copy(self):
        return FloatRect(self._left, self._top, self._width, self._height)

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, val):
        self._top = val

    @property
    def bottom(self):
        return self._top + self._height

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, val):
        self._left = val

    @property  
    def right(self):
        return self._left + self._width