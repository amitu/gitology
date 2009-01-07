==============================
Gitology Getting Started Guide
==============================

** about **

Gitology is a knowledge-management system. It uses text files to store data, 
in a special directory called a gitology repository. Gitology repository itself is 
under a version control system. As of now only `git` is supported as RCS backend.

** gitology repository **

Gitology repository is designed to be accessed manually. The structure of 
gitology repository is explained in `gitology-repo-structure.txt`. Standard tools
like `vim`, `ls`, `grep`, `find`, `cat` etc can be used to work with gitology 
repo. Gitology also comes with a set of command line scripts to help in common 
operations on gitology repository.

** gitology repository lookup protocol **

Gitology repository can be located anywhere on the file system. Its location and 
few other gitology related configurations are stored in a rc file. By default 
configuration file is called `.gitologyrc` on unix like systems and `_gitology`
under windows. The file is located in `$HOME` directory of the user. 

Note: The location of configuration file can also be specified in an environment 
variable called `GITOLOGY_CONFIG_FILE`. 

** creating a gitology repository **

New gitology repository can be created using `gitology-init` command. This command
comes as a part of gitology. To create gitology repository named `gitology_repo`,
located under `~/Documents/` folder, run the command `gitology-init 
~/Documents/gitology_repo`. This command will check and create a gitology 
configuration file, `.gitology`, containing the location of newly created repository.

** gitology document **

Gitology organized the knowledge in a primitive called a gitology `document`. The 
document has a unique name, and is composed of content, meta data, comments on 
the document, dependencies and versions. Gitology documents are stored in a 
directory called `documents` in gitology repository. Each document is stored as
a directory named after the document's name. For this reason document's name
should be a valid file name. The name of the document is for internal use only.
Document supports meta data store which can be used for storing more meaningful
title of the document. 

Note: Some operating systems do not support large number of files in a directory. 
This could be a problem if the gitology repository starts to become too big, 
and reaches the file system limits of the operating system. Gitology comes with a 
feature that can be used to work around this by further creating subdirectories 
inside document folder. Gitology uses md5 based naming scheme to overcome this 
limitation. This feature makes guessing the name of the folder, in which a 
document's data is store, difficult. Gitology ships with md5 use diabled. It can 
be enabled by adding `USE_MD5=True` under `REPO` section of `.gitologyrc` file. 
Gitology repository with support of thie feature can be created by supplying `--md5`
flag to `gitology-init` command, eg: `gitology-init --md5 ~/Document/gitology_repo`.
`gitology-convert-repo --to-md5` or `gitology-convert-repo --to-flat` can be used
to convert existing repositores. 

~/Documents/gitology_repo/
  +- documents/
  |   +- hello_word/
  |   |   +- index.rst/index.html/index.txt
  |   |   +- meta.json
  |   |   +- replies/
  |   |   |   +-  0/
  |   |   |   +-  2/
  |   |   |   ...
  |   |   +- deps
  |   |   |   +- hello_world.gif
  |   |   |   +- hello_world.py
  |   |   |   ...

The document can store its primary content in either a text file, an html file or as
a restructured text document. Other content formats would be supported in future.
The format of the content is deduced from the name of the content file, which is called
`index`. 

Meta data on document are stored in a file called `meta.json`. Meta data is stored as 
`key-value` pairs, and any arbitrary data can be stored as meta data. Typically each 
document has meta data about the `author` of the document, `created_on`, and 
`last_modified_on`, and `type`. None of these data are required. 

Each document can have replies associated with this document. The replies are stored in 
a folder called `replies`. Each reply itself contains an `index`, which follows the same
index guideline as that for `documents`. Each reply can also have meta data to store 
the name of the person who created that reply or when was it created etc. Replies can have
further replies, so a tree like comment system for each document can be implemented with
gitology. 

Further, each document can have a set of dependencies, stored in a folder called `deps`. 

Everything in the document is under version control. `gitology python module` or `git`
can be used to find out history of each file in the document. 


** gitology python api **

Gitology comes with a python package to work with gitology repositories. By default 
gitology package also follows the gitologyrc lookup protocol described above to find
the gitology repository to work on. This package also contains methods to 
programmatically specify the repository location and other configuration options.
As of now, gitology configurations can not be changed on runtime. `gitology.config.settings`
contains settings that are read from `gitologyrc` file, or specified programmatically.

The main class to work with documents in gitology is `gitology.documents.Document`. It 
takes document name in constructor and provides access to index(`Document.index`), 
replies(`Document.replies`), dependencies(`Document.deps`), and meta data(`Document.meta`), 
about it. 

Gitology package also contains `gitology.revisions` module to look up history of any part
of the document. 

Furhter API reference can be looked up in the `api.rst` file. 

** gitology repo meta files **

Gitology repository contains a file called `editors.txt`. This file contains the list 
of `openids` of users who are allowed to edit documents. Each document can contain a meta
data called `editors`. This can be used to specify edit permission on per document basis.
This feature is used only when gitology document is being modified from web. 

Gitology repository contains a file called `blocked-authors.txt`. This file contains a 
list of users who are not given any permissions on any document in this repository. This 
is also used only when gitology web application is being used to modify document from 
browser. 

** gitology blogs **

Knowledge stored in Gitology repository can also be accessed via web in form of 
blog and wiki. 

Installing Gitology
-------------------

Gitology is composed of gitology-core and gitology.d, a django application. 

Gitology core consists of a set of command line scripts to manage gitology-repo, and 
a django app to expose the repo on web.

Gitology core dependencies:

#. Python 2.4 or above
#. Django 1.0 or above.
#. git

Installing gitology
===================

$ git clone http://repo.or.cz/r/gitology.git
$ cd gitology

To test gitology before installing, do the following:

$ python setup.py test
$ sudo python setup.py install

To test gitology works:

$ gitology --version
0.1
$ 

Getting Started with Gitology
=============================

Gitoloy stores all blog and wiki data in text files under a repo, which 
itself is under revision control using git. 

To create the repo, use gitology-init script. Go the folder that 

$ gitol


Gitololgy.d, django app dependencies:

#. gitology core
#. Django 1.0 or above
#. python-yadis
#. python-openid 2.2.1 or above
#. django-openid [branch=openid-2.0+auth]
#. docutils

Django:

First confirm that you don't have old version of django installed.

$ python
>>> import django
>>> django
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ImportError: No module named django
>>> 

If you don't get the above exceptiom, you may have some django installed. Check its version:

$ python
>>> import django
>>> django.VERSION
>>> django.VERSION
(1, 0, 'final')
>>> 

Any this less than 1.0 is not supported. 

How to delete old version of django:

$ python 
>>> import django
>>> django
<module 'django' from '/home/amitu/Projects/Django/django/__init__.pyc'>
>>> raise SystemExit
$ rm -rf $(the folder that contains old django). 

Get new django:

$ wget http://www.djangoproject.com/download/1.0.2/tarball/
$ tar -xzf Django-1.0.2-final.tar.gz
$ cd Django-1.0.2-final
$ sudo python setup.py install

Installing python-yadis:

$ sudo easy_install python-yadis

If you get an error saying command not found for easy_install, install 
setuptools first:

$ sudo apt-get install python-setuptools

Installing python-openid 2.2.1:

$ wget http://openidenabled.com/files/python-openid/packages/python-openid-2.2.1.tar.gz
$ tar -xzf python-openid-2.2.1.tar.gz
$ cd python-openid-2.2.1
$ sudo python setup.py install 

Installing django-openid:

$ svn checkout http://django-openid.googlecode.com/svn/branches/openid-2.0+auth/django_openidconsumer

Because django-openid does not come with an installation method as yet, you will have to 
manually copy it on of the folders in python's path. To get the system folders on python 
path, do the following:

$ python
>>> import sys
>>> print sys.path

It will list a directories, copy django_openidconsumer in any of the directories there.

Installind docutils:

$ sudo apt-get install python-docutils


Understanding gitology
======================

Gitology stores data in text files, and these text files, and version data in git. 
(in future other revision control systems will be supported)

To start git

Configuring gitology

