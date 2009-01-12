"""
config module

This module reads config.

By default it reads config from ~/.gitologyrc.

If environment variable GITOLOGY_CONFIG_FILE set and contains a filename it reads from that file. 

If file_name is passed, it will be used.
"""

import ConfigParser, os, path
from gitology.utils import attrdict, ImproperlyConfigured

def get_config(file_name=None):
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    _config = attrdict()
    if file_name:
        _config.RC_FILE = path.path(os.path.expanduser(file_name))
    elif "GITOLOGY_CONFIG_FILE" in os.environ:
        _config.RC_FILE = path.path(
            os.path.expanduser(os.environ["GITOLOGY_CONFIG_FILE"])
        )
    else: 
        _config.RC_FILE = path.path(os.path.expanduser("~/.gitologyrc"))
    if not _config.RC_FILE.exists(): 
        raise ImproperlyConfigured("RC file does not exists: %s" % _config.RC_FILE.abspath())
    config.read(_config.RC_FILE) 
    for section in config.sections():
        _config[section] = attrdict()
        for k, v in config.items(section):
            _config[section][k] = v
    return _config

def initialize():
    conf = get_config()
    if "REPO" not in conf: 
        raise ImproperlyConfigured("No section REPO in config, file=%s." % conf.RC_FILE)
    if "LOCAL" not in conf.REPO: 
        raise ImproperlyConfigured("No setting LOCAL in REPO, file=%s." % conf.RC_FILE)
    if "REMOTE" not in conf.REPO: conf.REPO.REMOTE = ""
    if "AUTO_COMMIT" in conf.REPO: 
        conf.REPO.AUTO_COMMIT = { 'True': True }.get(conf.REPO.AUTO_COMMIT, False)
        if conf.REPO.AUTO_COMMIT and not conf.REPO.REMOTE:
            raise ImproperlyConfigured("AUTO_COMMIT is set, but remote is not specified. file=%s" % conf.RC_FILE)
    else: conf.REPO.AUTO_COMMIT = False
    if "DEFAULTS" not in conf:
        raise ImproperlyConfigured("No section DEFAULTS in config, file=%s." % conf.RC_FILE)
    if "AUTHOR" not in conf.DEFAULTS: 
        raise ImproperlyConfigured("No setting AUTHOR in DEFAULTS, file=%s." % conf.RC_FILE)
    if not conf.DEFAULTS.AUTHOR:
        raise ImproperlyConfigured("AUTHOR must not be empty, file=%s." % conf.RC_FILE)
    if "USE_MD5" not in conf.DEFAULTS: 
        conf.DEFAULTS.USE_MD5 = False
    else:
        conf.DEFAULTS.USE_MD5 = { 'True': True }.get(conf.DEFAULTS.USE_MD5, False)
    conf.LOCAL_REPO_PATH = path.path(os.path.expanduser(conf.REPO.LOCAL))
    import gitter
    gitter.git = gitter.Git(conf.REPO.LOCAL, conf.REPO.REMOTE, conf.REPO.AUTO_COMMIT)
    return conf
    
settings = initialize() # some app may override this property afterwards.

if __name__ == "__main__":
    import doctest
    doctest.testmod()
