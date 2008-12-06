# doc {{{
"""
This modules is used to talk with git.

>>> from gitology.gitter import Git
>>> git = Git("local", "remote")
>>>
"""
# }}}

import os, path
from gitology.utils import NamedObject

class Git(object):
    def __init__(self, local_path, remote_path=None, auto_push=True):
        self.local_path = local_path
        self.remote_path = remote_path
        self.auto_push = auto_push
    
    # local_path {{{
    def _get_local_path(self): return self._local_path
    def _set_local_path(self, new_path): 
        self._local_path = path.path(os.path.expanduser(new_path))
    
    local_path = property(
        _get_local_path, _set_local_path,
        doc = """
        >>> from gitology.gitter import Git
        >>> git = Git("/some/path")
        >>> git.local_path 
        path('/some/path')
        >>> git.local_path = '/someother/path'
        >>> git.local_path
        path('/someother/path')
        >>> git.remote_path
        >>> 
        """
    )
    # }}}
    # remote_path # {{{
    def _get_remote_path(self): return self._remote_path
    def _set_remote_path(self, new_path): 
        self._remote_path = new_path

    remote_path = property(
        _get_remote_path, _set_remote_path, 
        doc = """
        >>> from gitology.gitter import Git
        >>> git = Git("local", "remote")
        >>> git.local_path, git.remote_path
        (path('local'), 'remote')
        """
    )
    # }}}

    def check(self):
        """ 
        This checks if the local repo is valid, it will perform the following
        tests:
            * see if folder exists
            * see if its a valid git repo
        """

    def init_local_repo(self):
        """
        If self.check() fails, it might mean a new repo, this function will
        create new repo in the lcoal path. It will first try to clone from 
        the remote repo. If no remote is specified, it will create a new local
        repo. 
        """

    def revert(self):
        """ 
        revert cleans up all change in repo. be careful about using it.
        """

    def commit(self, msg):
        """
        commit -a everything with specified message.
        """

    def add(self, fpath="."):
        """ 
        add the path in git repo.
        """

    def remove(self, fpath):
        """
        git rm -f path
        """

    def push(self):
        """
        push it to remote repo.
        """

    def pull(self):
        """ git pull remote self.remote_path """

    def sync(self):
        """ self.pull() self.push() """

class FileRevisions(NamedObject): pass
class Revision(object): pass

if __name__ == "__main__":
    import doctest
    doctest.testmod()
