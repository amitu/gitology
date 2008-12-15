"""
Various utility functions used by gitology.*
"""
import docutils.writers.html4css1, docutils.core

def path2obj(path):
    from django.core.urlresolvers import get_mod_func
    mod_name, obj_name = get_mod_func(path)
    obj = getattr(__import__(mod_name, {}, {}, ['']), obj_name)

def text_to_html(text_input):
    return "<pre>%s</pre>" % text_input

def rest_to_html(rest_input, css_path=None):
    """Render ReStructuredText."""
    writer = docutils.writers.html4css1.Writer()
    from gitology.config import settings
    import os.path
    if css_path is None and "DEFAULT_REST_CSS" in settings.DEFAULTS:
        css_path = os.path.expanduser(settings.DEFAULTS.DEFAULT_REST_CSS)
    docutils.core.publish_string(
        rest_input, writer=writer,
        settings_overrides={
            'stylesheet': css_path,
            'stylesheet_path': None,
            'embed_stylesheet': True
        }
    )
    return writer.output

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

class NamedObject(object):
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
