"""
Various utility functions used by gitology.*
"""
# imports # {{{
from django.conf.urls.defaults import patterns
from django.utils import simplejson

import path, sys, os, textwrap
import fnmatch, re, path
import gzip, bz2
import docutils.writers.html4css1, docutils.core
from odict import OrderedDict as odict
# }}}

class ImproperlyConfigured(Exception): pass

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
    return docutils.core.publish_parts(
        rest_input, writer_name="html", settings_overrides={
            'stylesheet': css_path,
            'stylesheet_path': None,
            'embed_stylesheet': True
        }
    )['html_body']
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
    def __unicode__(self): 
        return u"%s(%s)" % ( self.__class__.__name__, self.name )
    __str__ = __unicode__
    __repr__ = __unicode__
# }}}

# get_blog_data # {{{
class list_with_clone(list):
    def _clone(self): return self

global_blog_dict = {}
def get_blog_data(p):
    from gitology.document import Document
    blog = {}
    blog["name"] = p.basename()
    blog["document"] = Document("blogs@%s" % blog["name"])
    if p.basename() == "main": blog["prefix"] = "blog/"
    else: blog["prefix"] = "%s/" % p.basename()
    # posts
    blog["posts"] = odict()
    years = p.dirs()
    years.sort()
    for y in years:
        if y.namebase == "labels": continue
        months = y.dirs()
        months.sort()
        for m in months:
            dates = m.glob("*.lst")
            dates.sort()
            for d in dates:
                for l in d.open().readlines():
                    # format: url document_name timestamp
                    url, document_name, timestamp = l.split(" ", 2)
                    blog["posts"][url] = { 
                        'date': timestamp, 'document': Document(document_name),
                    }
                    global_blog_dict[url] = blog
    blog["posts"].reverse()
    # labels
    blog["labels"] = {}
    for l in p.joinpath("labels").glob("*.lst"):
        d = {}
        d["name"] = l.namebase
        d["posts"] = list_with_clone()
        d["document"] = Document("blogs@%s@label@%s" % (blog["name"], l.namebase))
        for line in l.open().readlines():
            # format: url, data is in respective archive file
            d["posts"].append(blog["posts"][line.strip()])
            blog["posts"][line.strip()].setdefault("labels", []).append(d)
        blog["labels"][l.namebase] = d
    return blog
# }}}

# get_blog {{{ 
def get_blog(p):
    urls = []
    b = get_blog_data(p)
    urls.append(
        ("%s$" % b["prefix"], "gitology.d.views.show_blog", { 'blog_data': b,})
    )
    urls.append(
        (
            "%slabelled/(?P<label_name>[^/]+)/$" % b["prefix"], 
            "gitology.d.views.show_category", { 'blog_data': b },
        )
    )
    from django.contrib.syndication.feeds import Feed
    class LatestEntries(Feed):
        title = b["document"].meta.title
        link = b["document"].meta.title
        description = b["document"].meta.subtitle

        def items(self):
            return b["posts"].values()[:10]

        def item_link(self, item): 
            return item["document"].meta.url

    feeds = { 'latest': LatestEntries }

    urls.append(
        (
            '%sfeeds/(?P<url>.*)/$' % b["prefix"], 
            'django.contrib.syndication.views.feed',
            {'feed_dict': feeds},
        )
    )
    return urls
# }}}

# get_blogs # {{{
def get_blogs():
    from gitology.config import settings as gsettings
    urls = []
    blogs_folder = gsettings.LOCAL_REPO_PATH.joinpath("blogs")
    for d in blogs_folder.dirs():
        urls += get_blog(d)
    return urls
# }}}

# get_wiki # {{{
global_wiki_dict = {}
def get_wiki():
    from gitology.config import settings as gsettings
    from gitology.document import Document
    urls = []
    wiki_folder = gsettings.LOCAL_REPO_PATH.joinpath("wiki")
    for i in wiki_folder.walk():
        if not i.isfile(): continue
        wiki_document = Document(i.open().read().strip())
        wiki_url = i[len(wiki_folder):-4] + "/"
        global_wiki_dict[wiki_url] = wiki_document
    return urls
# }}}

# refresh_urlconf_cache # {{{
def refresh_urlconf_cache():
    print "refresh_urlconf_cache"
    from gitology.config import settings
    """ creates a urlconf that is stored """
    global_blog_dict = {}
    global_wiki_dict = {}
    urls = [''] 
    # for blog:
    # list of blogs is in $reporoot/blogs/
    # urls: /blog_name/
    # blog named "main" goes under /blog/, rest of them go to /folder_name/
    urls += get_blogs() 
    urls += get_wiki()
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
    #print urls
    return urls
# }}}

# sort_nicely # {{{
# http://nedbatchelder.com/blog/200712/human_sorting.html
import re
def tryint(s):
    try: return int(s)
    except: return s
    
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
# }}}

# smart_wrap # {{{
def smart_wrap(s, width=None):
    if width is None:
        width = int(os.environ.get("COLUMNS", 70))
    lines = []
    for line in s.split("\n"):
        if not line.split(): lines.append("")
        else: lines += textwrap.wrap(line, width=width)
    return "\n".join(lines)
# }}}

# getDirSize {{{ 
# stolen from: http://mail.python.org/pipermail/python-list/2000-June/037460.html
def calcDirSize(arg, dir, files):
    for file in files:
        stats = os.stat(os.path.join(dir, file))
        size = stats[6]
        arg.append(size)

def getDirSize(dir):
    sizes = []
    os.path.walk(dir, calcDirSize, sizes)
    total = 0
    for size in sizes:
        total = total + size
    if total > 1073741824:
        return (round(total/1073741824.0, 2), 'GB')
    if total > 1048576:
        return (round(total/1048576.0, 2), 'MB')
    if total > 1024:
        return (round(total/1024.0, 2), 'KB')
    return (total, 'bytes')
# }}}

# generators from http://www.dabeaz.com/generators/
# these generators are one time use only

# use http://www.fiber-space.de/generator_tools/doc/generator_tools.html 
# for copying generators.

def gen_find(filepat,top=""):
    if not top: top = path.path(".").abspath()
    top = os.path.expanduser(top)
    for path_, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path_, name)

def gen_exclude(pattern, lines):
    patter = re.compile(pattern)
    for line in lines:
        if not re.search(pattern, line):
            yield line
    
def gen_grep(pattern, lines):
    patter = re.compile(pattern)
    for line in lines:
        if re.search(pattern, line):
            yield line

def gen_open(filenames):
    for name in filenames:
        if name.endswith(".gz"):
              yield gzip.open(name)
        elif name.endswith(".bz2"):
              yield bz2.BZ2File(name)
        else:
              yield open(name)

def gen_cat(sources):
    for s in sources:
        for item in s:
            yield item

def counter(gen):
    c = 0
    for item in gen: c += 1
    return c 
