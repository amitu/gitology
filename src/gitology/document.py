"""
document module
---------------
This module gives access to a document. This is the crux of gitology backend.
"""
from gitology.config import settings
from gitology import DocumentBase

import md5

class DocumentAlreadyExists(Exception): pass
class DocumentDoesNotExists(Exception): pass

class DocumentMeta(DocumentBase): pass
class DocumentDependencies(DocumentBase): pass

class Replies(DocumentBase): pass
class Comment(object): pass

class Document(DocumentBase):
    def __init__(self, name):
        """
        Calling the constructor does not do much, to see if document exists,
        call document.exists() function, and to create it, call 
        document.create().
        """
        super(Document, self).__init__(name)
   
    @property 
    def fs_path(self):
        md5sum = md5.new(self.name).hexdigest()
        return settings.LOCAL_REPO_PATH.joinpath(
            "documents/%s/%s/%s" % (md5sum[:2], md5sum[2:4], self.name)
        )

    def exists(self):
        e = self.fs_path.exists()
        if e: assert self.fs_path.isdir(), "Document path(%s) exists but is not a directory." % self.fs_path
        return e

    def create(self, index_content, author=None, format="rst"):
        """ 
        Creates the document with specified content. the name of index file
        is "index.%s" % format. 
    
        author is openid of the author who created this document. 
        
        This raises DocumentAlreadyExists if document already exists. 
        """
        if self.exists(): raise DocumentAlreadyExists
        if not author:
            author = settings.DEFAULTS.AUTHOR
        assert_author_can_write(author)
        self.fs_path.makedirs()
        self.replies.create()
        self.meta.create()
        self.meta.author = author
        self.fs_path.joinpath("index.%s" % format).write_text()
        
    def get_index(self):
        """
        Get the index content. If index was rst, it will be converted to html.
        If index was plain text, <pre></pre> version will be returned. 
    
        Raises DocumentDoesNotExists if.
        """
    index = property(get_index)
    
    def get_index_name(self):
        """
        """
    index_name = property(get_index_name)

    def get_index_format(self):
        """
        """ 
    format = property(get_index_format)

    def set_raw_index(self, content, format=None):
        """
        This sets the current index to what has been passed. Optionally this
        can change the type of index, if format is not None, in which case old
        index may be deleted.
        
        Raises DocumentDoesNotExists if.
        """

    def _get_meta(self):
        if hasattr(self, "_meta"): return self._meta
        if self.exists():
            self._meta = DocumentMeta(self.name)
            return self._meta
        else: raise DocumentDoesNotExists
    meta = property(_get_meta)

    def _get_deps(self):
        if hasattr(self, "_deps"): return self._deps
        if self.exists():
            self._deps = DocumentDependencies(self.name)
            return self._deps
        else: raise DocumentDoesNotExists
    deps = property(_get_deps)

    def _get_replies(self):
        if hasattr(self, "_replies"): return self._replies
        if self.exists():
            self._replies = Replies("%s/comments", self.name)
            return self._replies
        else: raise DocumentDoesNotExists
    replies = property(_get_replies)

    def _get_revisions(self):
        if hasattr(self, "_revisions"): return self._revisions
        if self.exists():
            self._revisions = FileRevisions("%s/%s", (self.name, self.index_name))
            return self._revisions
        else: raise DocumentDoesNotExists
    revisions = property(_get_revisions)

def assert_author_can_write(author):
    pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
