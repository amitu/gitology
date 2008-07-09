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
