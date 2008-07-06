"""
config module

This module reads config.

By default it reads config from ~/.gitologyrc.

If environment variable GITOLOGY_CONFIG_FILE set and contains a filename it reads from that file. 

If file_name is passed, it will be used.
"""

import ConfigParser, os

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

def get_config(file_name=None):
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    if file_name:
        config.read(os.path.expanduser(file_name))
    elif "GITOLOGY_CONFIG_FILE" in os.environ:
        config.read(os.environ["GITOLOGY_CONFIG_FILE"])
    else: 
        config.read(os.path.expanduser("~/.gitology")) 
    _config = attrdict()
    for section in config.sections():
        _config[section] = attrdict()
        for k, v in config.items(section):
            _config[section][k] = v
    return _config

