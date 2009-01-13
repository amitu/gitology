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
>>> python_document.index
u'<div class="document" id="python">\n<h1 class="title">Python</h1>\n<p>get md5: import md5; md5.new(&quot;amit upadhyay&quot;).hexdigest()</p>\n</div>\n'
>>> python_document.index_name
'index.rst'
>>> python_document.format
'rst'

Meta data is stored:

>>> python_document.meta.some_meta_data
42
>>> "fs_path" in python_document.meta 
True

Replies:

>>> python_document.replies
Replies(gitology-sample-repo/documents/python/replies)
>>> python_document.replies.fs_path.endswith("gitology-sample-repo/documents/python/replies")
True
>>> len(python_document.replies)
1
>>> python_document.replies.count()
1
>>> 

Analyzing a single comment:
>>> comment = python_document.replies[0]
>>> comment.name.endswith('/gitology-sample-repo/documents/python/replies/1')
True
>>> comment.index_name
'index.rst'
>>> comment.index
u'<div class="document">\n<p>python sucks!</p>\n</div>\n'
>>> # python_document.replies.append(author_name="amit upadhyay", comment_content="this rocks")
>>>

>>> asd_document = Document("asd")
>>> asd_document.exists()
True
>>> asd_document.replies.count()
0
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
