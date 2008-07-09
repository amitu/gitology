"""
config module

This module reads config.

By default it reads config from ~/.gitologyrc.

If environment variable GITOLOGY_CONFIG_FILE set and contains a filename it reads from that file. 

If file_name is passed, it will be used.
"""

import ConfigParser, os, path

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
    _config = attrdict()
    if file_name:
        _config.RC_FILE = os.path.expanduser(file_name)
    elif "GITOLOGY_CONFIG_FILE" in os.environ:
        _config.RC_FILE = os.path.expanduser(os.environ["GITOLOGY_CONFIG_FILE"])
    else: 
        _config.RC_FILE = os.path.expanduser("~/.gitologyrc") 
    config.read(_config.RC_FILE) 
    for section in config.sections():
        _config[section] = attrdict()
        for k, v in config.items(section):
            _config[section][k] = v
    return _config

class ImproperlyConfigured(Exception): pass

def initialize():
    conf = get_config()
    if "REPO" not in conf: 
        raise ImproperlyConfigured("No section REPO in config, file=%s." % conf.RC_FILE)
    if "LOCAL" not in conf.REPO: 
        raise ImproperlyConfigured("No section LOCAL in REPO, file=%s." % conf.RC_FILE)
    conf.LOCAL_REPO_PATH = path.path(os.path.expanduser(conf.REPO.LOCAL))
    return conf
    
settings = initialize() # some app may override this property afterwards.

if __name__ == "__main__":
    import doctest
    doctest.testmod()
