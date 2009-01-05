"""
Gitology Test Suite
===================

To run tests do the following:

$ python setup.py test

Tests against the gitology-sample-repo, and amitucom webapp.

Basic setup
-----------
#doctest +ELLIPSIS

>>> import os, sys
>>> os.environ["GITOLOGY_CONFIG_FILE"] = "gitologyrc"
>>> os.environ["DJANGO_SETTINGS_PATH"] = "amitucom.settings"
>>> sys.path.append("/home/amitu/Projects/Django")

>>> from gitology.document import Document
>>> from gitology.config import settings as gsettings
>>> python_document = Document("python")
>>> python_document.exists()
True
>>> Document("non_existant_document").exists()
False

Testing basic properties of a document:

>>> python_document.name
'python'
>>> python_document.fs_path
path('gitology-sample-repo/documents/python')
>>>

Meta data is stored:

>>> python_document.meta.some_meta_data
42
>>> "fs_path" in python_document.meta 
True

Replies:

>>> python_document.replies
Replies(gitology-sample-repo/documents/python/comments)
>>> python_document.replies.fs_path.endswith("gitology-sample-repo/documents/python/comments")
True
>>> len(python_document.replies)
3
>>> python_document.replies.count()
4
>>> 
"""

import unittest
import doctest
suite = unittest.TestSuite()
suite.addTest(
    doctest.DocFileSuite("tests.py", optionflags=doctest.ELLIPSIS)
)

if __name__ == "__main__":
    #doctest.testmod()
    unittest.TextTestRunner().run(suite)
