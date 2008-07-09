# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/361668
class attrdict(dict):
    """A dict whose items can also be accessed as member variables.

    >>> d = attrdict(a=1, b=2)
    >>> d['c'] = 3
    >>> print d.a, d.b, d.c
    1 2 3
    >>> d.b = 10
    >>> print d['b']
    10

    # but be careful, it's easy to hide methods
    >>> print d.get('c')
    3
    >>> d['get'] = 4
    >>> print d.get('a')
    Traceback (most recent call last):
    TypeError: 'int' object is not callable
    """
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

class DocumentBase(object):
    def __init__(self, name): 
        self._name = name
    def _get_name(self): return self._name
    name = property(
        _get_name, doc="""
            self.name is readonly.

            >>> d = DocumentMeta("somename")
            >>> d.name
            'somename'
            >>> d.name = "new name"
            Traceback (most recent call last):
                ...
            AttributeError: can't set attribute
            >>>
        """
    )
