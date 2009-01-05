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

Meta data is stored:

>>> python_document.meta.some_meta_data
42
>>> "fs_path" in python_document.meta 
True

Replies:

>>> python_document.replies
<gitology.document.Replies object at 0x...>
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
