"""
Gitology Test Suite
===================

To run tests do the following:

$ python setup.py test

Tests against the gitology-sample-repo, and amitucom webapp.

Basic setup
-----------

>>> import os, sys
>>> os.environ["GITOLOGY_CONFIG_FILE"] = "gitologyrc"
>>> os.environ["DJANGO_SETTINGS_PATH"] = "amitucom.settings"
>>> sys.path.append("/home/amitu/Projects/Django")

>>> from gitology.document import Document
>>> from gitology.config import settings as gsettings
>>> Document("python").exists()
True
>>>
"""

import unittest
import doctest
suite = unittest.TestSuite()
suite.addTest(doctest.DocFileSuite("tests.py"))

if __name__ == "__main__":
    #doctest.testmod()
    unittest.TextTestRunner().run(suite)
