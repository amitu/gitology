"""
Various utility functions used by gitology.*
"""
# imports # {{{
from django.conf.urls.defaults import patterns
from django.utils import simplejson

import path, sys
import docutils.writers.html4css1, docutils.core
# }}}

# path2obj # {{{
def path2obj(path):
    from django.core.urlresolvers import get_mod_func
    mod_name, obj_name = get_mod_func(path)
    return getattr(__import__(mod_name, {}, {}, ['']), obj_name)
# }}}

def text_to_html(text_input): return "<pre>%s</pre>" % text_input

# rest_to_html # {{{
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
# }}}

# attrdict # {{{
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
# }}}

# NamedObject # {{{
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
# }}}

# get_blog_data # {{{
def get_blog_data(p):
    from gitology.document import Document
    blog = {}
    blog["name"] = p.basename()
    if p.basename() == "main": blog["prefix"] = "blog/"
    else: blog["prefix"] = "%s/" % p.basename()
    # posts
    blog["posts"] = {}
    for y in p.dirs():
        if y.namebase == "labels": continue
        for m in y.dirs():
            for d in m.glob("*.lst"):
                for l in d.open().readlines():
                    blog["posts"][l.strip()] = { 
                        'date': d, 'document': Document(l.strip()),
                    }
    # labels
    blog["labels"] = []
    for l in p.joinpath("labels").glob("*.lst"):
        d = {}
        d["name"] = l.namebase
        d["posts"] = []
        for l in l.open().readlines():
            d["posts"].append(blog["posts"][l.strip()]['document'])
        blog["labels"].append(d)
    return blog
# }}}

# get_blog {{{ 
def get_blog(p):
    urls = []
    b = get_blog_data(p)
    urls.append(("%s$" % b["prefix"], "show_blog", { 'blog_data': b,}))
    for l in b["labels"]:
        urls.append(
            (
                "%slabelled/%s/$" % (b["prefix"], l["name"]), "show_category",
                { 'blog_data': b, 'category_data': l },
            )
        )
    return urls
# }}}

# get_blogs # {{{
def get_blogs():
    from gitology.config import settings
    urls = []
    blogs_folder = settings.LOCAL_REPO_PATH.joinpath("blogs")
    for d in blogs_folder.dirs():
        urls += get_blog(d)
    return urls
# }}}

# refresh_urlconf_cache # {{{
def refresh_urlconf_cache():
    print "refresh_urlconf_cache"
    from gitology.config import settings
    """ creates a urlconf that is stored """
    urls = ['gitology.d.views'] 
    # for blog:
    # list of blogs is in $reporoot/blogs/
    # urls: /blog_name/
    # blog named "main" goes under /blog/, rest of them go to /folder_name/
    urls += get_blogs() 

    # for each blog, list of labels in $reporoot/blogs/blog_name/labels/ 
    # urls: /blog_name/label/label_name/
    # for each blog, date based heirarchy is kept in 
    # $reporoot/blogs/blog_name/year/month/date.lst
    # /blog_name/year/month/date/document_name/

    # for wiki:
    # list of wiki document names are in $reporoot/wiki/document_alias.txt
    # urls: /document_alias/
    # further heirarchy is maintained: 
    # $reporoot/wiki/document_alias/child_alias.txt
    # /document_alias/child_alias/ 

    # for notes:
    # notebooks are stored in $reporoot/notebooks/
    # urls: /notebook/ this is a dedicated app 

    # for albums:
    # list of albums are in $reporoot/albums/ album_name.meta, album_name.lst
    # urls: /album|gallery/album_name/ this is document. it can contain select 
    # few photos etc.
    # each photo is basically a document, its list is in the album_name.lst
    # each album photo ll have a thumbnail and caption meta data to be shown 
    # on album page/
    # /album/album_name/photos/ will list all photos, each photo may be in one 
    # or more albums. each photo can be a blog post too in one or more blogs

    # optimization: this info will be loaded from a file, and some other tool
    # is to update this file everytime something interesting happens.

    # this function returns a dict containing url to view mapping.
    file(settings.LOCAL_REPO_PATH.joinpath("urlconf.cache"), "w+").write(
        #simplejson.dumps(urls)
        "updated"
    )
    print urls
    return urls
# }}}

