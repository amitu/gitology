try:
    from django.utils import simpljson
except ImportError:
    try:
        import simplejson
    except ImportError:
        print """You don't have simplejson installed, get it from:
http://pypi.python.org/pypi/simplejson"""
        raise

def refresh_urlconf_cache():
    """ creates a urlconf that is stored """
    # for blog:
    # list of blogs is in $reporoot/blogs/
    # urls: /blog_name/
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

