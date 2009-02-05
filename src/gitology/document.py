"""
document module
---------------
This module gives access to a document. This is the crux of gitology backend.
"""
# imports # {{{
from gitology.config import settings
from gitology.utils import NamedObject, attrdict
from gitology.gitter import FileRevisions
from gitology import utils

import md5, path, time
from datetime import datetime

try:
    from django.utils import simplejson
except ImportError:
    import simplejson
# }}}

# exceptions # {{{
class DocumentAlreadyExists(Exception): pass
class DocumentDoesNotExists(Exception): pass
class WriteNotAllowed(Exception): pass
# }}}

# DocumentMeta # {{{
class DocumentMeta(attrdict): 
    """ 
    DocumentMeta Class

    This is a gitology.config.attrdict like class.
    """
    def __init__(self, file_path, *args, **kw):
        super(DocumentMeta, self).__init__(*args, **kw)
        self.fs_path = path.path(file_path).abspath()
        if self.fs_path.exists():
            d = simplejson.loads(self.fs_path.open().read())
            self.__dict__.update(d)

    def save(self):
        d = self.copy()
        del d["fs_path"]
        self.fs_path.write_text(simplejson.dumps(d))
# }}}

# DocumentDependencies # {{{
class DocumentDependencies(NamedObject):
    """ 
    its a proxy for the directory. 

    self.get_dir() returns the directory. use normal python 
    """ 
# }}}

# DocumentBase # {{{
class DocumentBase(NamedObject):
    def exists(self):
        e = self.fs_path.exists()
        if e: 
            assert self.fs_path.isdir(), (
                "Document path(%s) exists but is not a directory." % 
                self.fs_path
            )
        return e

    def create(self, index_content, author=None, format="rst"):
        """ 
        Creates the document with specified content. the name of index file
        is "index.%s" % format. 
    
        author is openid of the author who created this document. 
        
        This raises DocumentAlreadyExists if document already exists. 
        """
        if self.exists(): raise DocumentAlreadyExists(self.name)
        if not author:
            author = settings.DEFAULTS.AUTHOR
        assert_author_can_write(author)
        self.fs_path.makedirs()
        self.meta.author = author
        self.meta.save()
        self.fs_path.joinpath("index.%s" % format).write_text(index_content.encode("utf8"))
        return self

    def get_index(self):
        """
        Get the index content. If index was rst, it will be converted to html.
        If index was plain text, <pre></pre> version will be returned. 
    
        Raises DocumentDoesNotExists if.
        """
        if not self.exists(): raise DocumentDoesNotExists
        if self.fs_path.joinpath("index.rst").exists():
            return utils.rest_to_html(
                self.fs_path.joinpath("index.rst").open().read().decode("utf8") 
            )
        elif self.fs_path.joinpath("index.html").exists():
            return self.fs_path.joinpath("index.html").open().read().decode("utf8")
        elif self.fs_path.joinpath("index.txt").exists():
            return utils.text_to_html(
                self.fs_path.joinpath("index.txt").open().read().decode("utf8") 
            )
        raise DocumentDoesNotExists, "index does not exist"
    index = property(get_index)
    
    def get_index_name(self):
        """
        """
        if not self.exists(): raise DocumentDoesNotExists
        if self.fs_path.joinpath("index.rst").exists(): return "index.rst"
        elif self.fs_path.joinpath("index.html").exists(): return "index.html"
        elif self.fs_path.joinpath("index.txt").exists(): return "index.txt"
        raise DocumentDoesNotExists, "index does not exist"
    index_name = property(get_index_name)

    def get_index_format(self):
        """
        """ 
        return self.index_name.split(".")[-1]
    format = property(get_index_format)

    def set_raw_index(self, content, format=None):
        """
        This sets the current index to what has been passed. Optionally this
        can change the type of index, if format is not None, in which case old
        index may be deleted.
        
        Raises DocumentDoesNotExists if.
        """
        if format is None: format = self.format
        try:
            if format != self.format:
                self.fs_path.joinpath(self.index_name).remove()
        except DocumentDoesNotExists: pass
        self.fs_path.joinpath("index.%s" % format).write_text(content.encode("utf8"))

    def get_raw_index(self):
        """
        Raises DocumentDoesNotExists if.
        """
        return self.fs_path.joinpath(self.index_name).open().read().decode("utf8")
    raw_index = property(get_raw_index, set_raw_index)

    def _get_meta(self):
        if hasattr(self, "_meta"): return self._meta
        if self.exists():
            self._meta = DocumentMeta(self.fs_path.joinpath("meta.json"))
            return self._meta
        else: raise DocumentDoesNotExists(self.name)
    meta = property(_get_meta)

    def _get_replies(self):
        if hasattr(self, "_replies"): return self._replies
        if self.exists():
            self._replies = Replies("%s/replies" % self.fs_path)
            return self._replies
        else: raise DocumentDoesNotExists
    replies = property(_get_replies)

    def _get_revisions(self):
        if hasattr(self, "_revisions"): return self._revisions
        if self.exists():
            self._revisions = FileRevisions(
                "%s/%s" % (self.name, self.index_name)
            )
            return self._revisions
        else: raise DocumentDoesNotExists
    revs = property(_get_revisions)
# }}}

# Comment # {{{
class Comment(DocumentBase): 
    def __init__(self, name):
        super(Comment, self).__init__(name)
        self.fs_path = path.path(self.name)

    def gid(self):
        return self.fs_path.namebase
# }}}

# Replies # {{{
class Replies(NamedObject): 
    """ emulates a list like object containing comments """
    def __init__(self, name):
        super(Replies, self).__init__(name)
        self.fs_path = path.path(self.name)

    def count(self):
        "total number of replies, number of nodes in children subtree"
        if not self.fs_path.exists(): return 0
        c = 0
        for comment in self:
            c += len(comment.replies) + 1
        return c

    def __len__(self):
        "number of direct replies" 
        if not self.fs_path.exists(): return 0
        return len(self.fs_path.dirs())

    def __getitem__(self, k):
        if not self.fs_path.exists(): raise KeyError
        dirs = self.fs_path.dirs()
        utils.sort_nicely(dirs)
        return Comment(dirs[k].abspath())

    def append(
        self, author_name, comment_content, format="txt",
        author_openid="anonymous", on=None, email=None, url=None, 
    ): 
        if not self.fs_path.exists():
            self.fs_path.makedirs()
        # find comment name
        comment_id = str(time.time())
        comment = Comment(self.fs_path.joinpath(comment_id))
        comment.create(
            index_content=comment_content, author=author_openid
        )
        comment.meta.author_name = author_name
        comment.meta.author_email = email
        comment.meta.author_url = url
        comment.meta.author_openid = author_openid
        if not on: on = datetime.now()
        comment.meta.posted_on = str(on)
        comment.meta.save()
# }}}

# Document {{{
class Document(DocumentBase):
    @property 
    def fs_path(self):
        if settings.DEFAULTS.USE_MD5:
            md5sum = md5.new(self.name).hexdigest()
            return settings.LOCAL_REPO_PATH.joinpath(
                "documents/%s/%s/%s" % (md5sum[:2], md5sum[2:4], self.name)
            )
        else:
            return settings.LOCAL_REPO_PATH.joinpath(
                "documents/%s" % self.name
            )


        
    def _get_deps(self):
        if hasattr(self, "_deps"): return self._deps
        if self.exists():
            self._deps = DocumentDependencies(self.name)
            return self._deps
        else: raise DocumentDoesNotExists
    deps = property(_get_deps)

# }}}

# assert_author_can_write # {{{
def assert_author_can_write(author):
    """
    Will raise WriteNotAllowed if there is no permission.
    """
# }}}

if __name__ == "__main__":
    import doctest
    doctest.testmod()
