======================
Gitology Documentation
======================

about
-----

**Gitology is a knowledge-management system**. It uses text files to store
data, in a special directory called a gitology repository. Gitology repository
itself is under a version control system. As of now only `git` is supported as
RCS backend.

gitology repository
-------------------

**All knowldege base, articles, blog posts, wiki pages, albums ete; are stored
in a folder called gitology repository**. Gitology repository is designed to be
accessed manually. The structure of gitology repository is explained in
`gitology-repo-structure.txt`. Standard tools like `vim`, `ls`, `grep`, `find`,
`cat` etc can be used to work with gitology repo. Gitology also comes with a
set of command line scripts to help in common operations on gitology
repository.

**gitology repository lookup protocol**

Gitology repository can be located anywhere on the file system. Its location
and few other gitology related configurations are stored in a rc file. By
default **gitology configuration file is called** `.gitologyrc` **on unix like
systems and** `_gitology` **on windows**. The file is located in `$HOME`
directory of the user. 

    Note: The location of configuration file can also be specified in an
    environment variable called `GITOLOGY_CONFIG_FILE`. 

**creating a gitology repository**

New **gitology repository can be created using** `gitology-init` **command**.
This command comes as a part of gitology. To create gitology repository named
`gitology_repo`, located under `~/Documents/` folder, run the command
`gitology-init ~/Documents/gitology_repo`. This command will check and create a
gitology configuration file, `.gitology`, containing the location of newly
created repository.

**gitology repo meta files**

Gitology repository contains the following files:

editors.txt

  This file contains the list of `openids` of users who are allowed to edit
  documents.  Each document can contain a meta data called `editors`. This can
  be used to specify edit permission on per document basis.  This feature is
  used only when gitology document is being modified from web. 

blocked-authors.txt

  This file contains a list of users who are not given any permissions on any
  document in this repository. This is also used only when gitology web
  application is being used to modify document from browser. 

**gitology-info**

*Gitology comes with a utility called `gitology-info` to find information about
current gitology repository**. It follows the gitology repository lookup
protocol to find repository location. It can tell users about the following
information about the gitology repository:

- repository location 
- repository size 
- number of documents in repository
- number and other information about blogs in repository
- information about wiki pages managed by repository

`gitology-info` prints a summary about repository by default. It also has a lot
of comman line arguments to find out specific details mentioned above and more.
For more details about this command run `man gitology-ingo` or `gitology-info
--about`.

gitology document
-----------------

**Gitology organized the knowledge in a primitive called a gitology**
`document`.  The document has a unique name, and is composed of content, meta
data, comments on the document, dependencies and versions. **Gitology**
`documents` **are stored in a directory called** `documents` **in gitology
repository**. Each document is stored as a directory named after the document's
name. For this reason document's name should be a valid file name. The name of
the document is for internal use only. Document supports meta data store which
can be used for storing more meaningful title of the document. 

::

    ~/Documents/gitology_repo/
      |~ documents/
      |   |~ hello_word/
      |   |   |- index.rst/index.html/index.txt
      |   |   |- meta.json
      |   |   |~ replies/
      |   |   |   |+  0/
      |   |   |   |+  2/
      /   /   /   ...
      |   |   |~ deps
      |   |   |   |- hello_world.gif
      |   |   |   |- hello_world.py
      |   |   |   |+ somedir/
      /   /   /   ...
      /   /   ...
      /   ...
      |- editors.txt
      |- blocked-users.txt
      ...

The **document stores its primary content in either a text file**, an html file
or as a restructured text document. Other content formats would be supported in
future.  The format of the content is deduced from the name of the content
file, which is called `index`. 

**Meta data on document are stored in a file called** `meta.json`. Meta data is
stored as `key-value` pairs, and any arbitrary data can be stored as meta data.
Typically each document has meta data about the `author` of the document,
`created_on`, and `last_modified_on`, and `type`. None of these data are
required. 

**Each document can have replies associated with this document**. The replies
are stored in folder called `replies`. Each reply itself contains an `index`,
which follows the same index guideline as that for `documents`. Each reply can
also have meta data to store the name of the person who created that reply or
when was it created etc. Replies can have further replies, so a tree like
comment system for each document can be implemented with gitology. 

Further, each document can have a set of dependencies, stored in a folder
called `deps`. 

Everything in the document is under version control. `gitology python module`
or `git` can be used to find out history of each file in the document. 

    Note: Some operating systems do not support large number of files in a
    directory.  This could be a problem if the gitology repository starts to
    become too big, and reaches the file system limits of the operating system.
    Gitology comes with a feature that can be used to work around this by
    further creating subdirectories inside document folder. Gitology uses md5
    based naming scheme to overcome this limitation. This feature makes
    guessing the name of the folder, in which a document's data is store,
    difficult. Gitology ships with md5 use diabled. It can be enabled by adding
    `USE_MD5=True` under `REPO` section of `.gitologyrc` file.  Gitology
    repository with support of thie feature can be created by supplying `--md5`
    flag to `gitology-init` command, eg: `gitology-init --md5
    ~/Document/gitology_repo`.  `gitology-convert-repo --to-md5` or
    `gitology-convert-repo --to-flat` can be used to convert existing
    repositores. 

gitology python api
--------------------

Gitology comes with a python package to work with gitology repositories. By
default gitology package also follows the gitologyrc lookup protocol described
above to find the gitology repository to work on. This package also contains
methods to programmatically specify the repository location and other
configuration options.  As of now, gitology configurations can not be changed
on runtime. `gitology.config.settings` contains settings that are read from
`gitologyrc` file, or specified programmatically.

The main class to work with documents in gitology is
`gitology.documents.Document`. It takes document name in constructor and
provides access to index(`Document.index`), replies(`Document.replies`),
dependencies(`Document.deps`), and meta data(`Document.meta`), about it. 

Gitology package also contains `gitology.revisions` module to look up history
of any part of the document. 

Furhter API reference can be looked up in the `api.rst` file. 

gitology blogs
---------------

**Gitology repository can be used as a blogs**. Gitology repository contains a
folder called `blogs` for this purpose. One gitology repository can have more
then one blogs. 

**blog meta data**

Each blog in gitology has a unique name. Information about that blog is kept in
a folder called `blogs/${blog_name}`. Names should be valid file names. Names
are also used to construct the url of the blog, the url is `/${blog_name}`. 

Blog name is exposed in blog's url, so it should be chosen accordingly. 

For each blog there is a gitology document, named: `blogs@${blog_name}`.

Example: for a blog named `links`, the data is stored in `blogs/links` folder
in gitology repository. The blog itself appears unders `/links/`. The document
for this blog is stored under the name `blogs@links`, physically stored in
`documents/blogs@links/` folder. 

The title of the blog is stored in `title` meta data of the blog document. A
blog typically has a tag line, which is stored in `subtitle` meta data of the
blog. Blog can also have longer description, stored in the `index` of the blog
document. 

Any document used as blog has `type` meta data `blog`.

To eash blog creation, gitology comes with a command `gitology-start-blog`. It
asks for blog name, title and subtitle and creates the document and blog folder
for you.  `gitology-alter-blog` can be used to change these properties of
existing blogs. 

**blog posts**

**Blog posts are stored as documents in gitology repository**. Any existing
document can be converted to blog post by using `gitology-blog-document`
command line tool.  This tool will ask for the blog name and name of the
document. It will pick the meta data `title` from the document if it exists,
otherwise it will prompt for the title. It will then check `url` meta data of
blog post document, if it does not exist it will prompt the user for it. Blog
post can have other meta data like `author`, `comments_allowed`,
`number_of_comments` etc. 

The content of post is stored in the document as its primary content, called
`document index`. 

To start a blog post from scratch, gitology comes with a commnd line tool
called `gitology-blog-new-post`. It will create a new document, ask for title,
and url; and open default editor of user to enter the post content. 

Any document that is used as a blog post is given a `type` meta data called
`blog_post`.

Gitology repository stores the connection between a blog post document, and 
the blog in the directory for the blog under `blogs/${blog_name}`. This folder
contains a folder for each year. It has folders named
`blogs/{%blog_name}/2008/`, `blogs/${blog_name/2009/` and so on. Each of these
year folders contains folders for months, eg `blogs/${blog_name/2008/01` for
posts in january of 2008, `blogs/${blog_name/2008/02` for posts in february
2008 and so on. Within each of the month folder, there are text files for each
date, eg `blogs/${blog_name/2008/02/01.lst` for posts on 1st of february 2008 
etc. The date text file contains one entry per line for each blog post. The 
format is: `/desired/url/of/post/ post_document_name 2008:02:01 04:30pm`. 

Gitology blog system does not enforce any URL scheme on blog posts. Users can
chose any scheme they prefer, `/writings/topic/` or `/blog/2008/02/07/topic/`
or even `/blog/2008/march/topic.html` and so on. 

Note: Gitology is designed with the mindset that a blog post can someday become
a wiki page if it gets popular and if author feels there is value in letting
others edit the post page. Gitology is also designed with the mindset that URLs
should not change, nor should there be duplication of content on multiple urls.
For all these reasons, using the term `blog` in url may be avoided, and more
generic url scheme should be preferred.

**Gitology ships with a django application that can be used to expose the blogs
stored in gitology repositories on web**. The application is called
`gitology.d`.  This application supports basic blog and threaded comments,
along with feeds. To learn how to use this application please see `installing
gitology.d` section. 

*offline online syncronization of gitology blog*

The web application lets you modify the post from the web. The comments posted
by visitors on web are stored in gitology repoistory under `replies` folder of
the document for that blog post. All these modifications are checked in the
revision control system used by gitology repository. The revision control
system can then be used to syncronize the gitology repository deployed on the
webserver with the one on author's local machine. 

**blog folder in gitology**

Information about post, its document name, the url, and the time it was
blogged, is stored under the blog special folder. Each blog special folder,
like `blogs/links/` mentioned for a blog named `links` contains the following
folder heirarchy.

:: 

    ~/Documents/gitology_repo/
      |~ documents/
      |   |+ hello_world/
      |   |~ blogs@links/
      |   |   |- index.rst
      |   |   |- meta.json
      /   /   ...
      |   |~ my_first_blog_post/
      |   |   |- index.rst
      |   |   |- meta.json
      |   |   |+ replies/
      |   |   |+ deps/
      /   /   ...
      |   |+ blog@links@labels@python/
      |   |+ blog@links@labels@opensource/
      /   ...
      |- editors.txt
      |- blocked-users.txt
      |~ blogs/
      |   |~ links/
      |   |   |~ labels
      |   |   |   |- python.lst
      |   |   |   |- opensource.lst
      |   |   |+ 2007
      |   |   |~ 2008
      |   |   |   |+ 01/
      |   |   |   |+ 02/
      |   |   |   |+ 03/
      |   |   |   |~ 04/
      |   |   |   |   |-01.lst
      |   |   |   |   |-02.lst
      |   |   |   |   |-03.lst
      /   /   /   /   ...
      |   |   |   |+ 05/
      /   /   /   ...
      |   |   |+ 2009/
      /   /   ...
      /   ...
      ...

**blog categories**

Gitology blogs support categories. Each post can have one or more categories.

Each category has a gitology `document` associated with it, containing meta
data and category description. The name of the `document` for category is based
on categories name and blog name. e.g. for a blog named `links`, and category
named `programming`, the name would be `blogs@links@labels@programming`. The
name of the category should be valid directory name. The actual title of the
category that is shown to the user is stored as meta data `title` on category
document. The url of category page is based on meta data `slug`, the url of
category page would be `/links/labelled/programming/` for the above example. 

A category is associated to a blog by means of a text file named after category
name. This text file resides in the folder
`blogs/${blog_name}/labels/%{category_name}.lst`. The text file contains the
urls of the blog posts that have this category. For example all posts in blog
`links` that belong to `programming` category are stored in the mentioned
`.lst` file, one url per line. Each post url can appear in one or more
category's `.lst` file.

The `document` for blog post also contains category information as document
meta data.  This is the master source of category information, and all category
`.lst` files can be generated based on this using the gitology tool
`gitology-refresh`. The category information stored in blog post document's
meta data will be updated by `gitology-blog-document`. 

    NOTE: `gitology-blog-document` comment can be used multiple time on the
    same blog document to update information about blog document. You can edit
    the title of a blog post or its categories after blogging it first, but
    rerunning this command line tool. 

gitology wiki
-------------

Gitology comes with a wiki system. Any `document` stored in gitology repository
can be exposed to web as a wiki page. Gitology wiki comes with fine grained
permission system to control who can view or edit the document online. 

To expose an existing `document` as wiki, gitology comes with a command line
tool call `gitology-wiki-document`. This command takes the name of the
`document` and the `url` at which it should be accessible, along with read and
write permissions. Gitology also comes with a command to create a new
`document` and simultaneously expose it to web as wiki, called
`gitology-wiki-new`. 

Gitology wiki does not enforce any url scheme. And documents can go to any
arbitrary url, `/wiki/python/` or `/articles/python/` or even
`/somepath/python.html` etc. Gitology is designed to make it easy for users to
convert a wiki document to blog post on a later date, or vice versa. For this
reason gitology recommends not using wiki as part of url, and organize document
urls in more natural fashion. 

Gitology repository contains a folder called `wiki`. If a document named
`python` is exposed to web on url `/python_tips/`, `gitology-wiki-document` or
`gitology-wiki-new` will create a file named `python_tips.txt` under the folder
`wiki`. This text file will contain the name of the document in it, in this
case `python`. URL heirarchy can be achieved by creating folder heirarchy in
`wiki` folder. eg to expose a document named `python` to web as wiki on the
url`/articles/python-tips/`, gitology will create
`wiki/articles/python-tips.txt`. This fille contain `python` which is the name
of the document. 

`gitology-wiki-document` can be called repeatedly on any `document` or url, to
alter the document name or url or any other meta data controlling wiki, for
example authorship permission.

Gitology wiki supports a threaded comment system. Comments are stored in
`replies` folder of the document that is exposed as wiki. 

Gitology web application can authenticate users using openid, and openid's of
users can be given permissions to view and or edit the document online.

gitology's django web application
=================================

Gitology comes with a package `gitology.d`. It is a django application and can
be plugged into any existing django website. Gitology source distribution comes
with an example project, `amitucom`, that can be used as starting point for
intigrating `gitology.d` with django projects. 

Gitology stores all its relevant files as text files in the gitology
repository. For this reason`gitology.d.models` do not expose any models. There
are basically some views and templates and a urls.py file connecting views to
urls. 

There are a lot of url's that are read from gitology repository and are not to
be hard coded in django project. Example include things like the names of
blogs, and their urls, wiki pages etc. Gitology dynamically constructs the
`urlconf` object in a middleware, `gitology.d.middleware.GitologyMiddleware`. 

For performace reason, `GitologyMiddleware` caches the `urlconf` object in
memory unless a text file, `gitology.cache` is updated.

Gitology comes with a utility called `gitology-refresh` that should be called
everytime something in gitology repository is changed that should change url
configuration, like a new post getting added to some blog or some old wiki
getting removed. Gitology tools like `gitology-blog-*`, `gitology-wiki-*`
automatically call `gitology-refresh` to keep things in sync. If gitology
repository has been modified by external commands, that gitology is designed to
facilitate, `gitology-refresh` should be called from time to time.

**adding gitology.d in a django project**

Follow the following steps to add `gitology.d` to a django project:

#. add 'gitology.d' to `INSTALLED_APPS` in `settings.py` so that `templatetags`
   shipped with gitology are available to templates.  

#. add the following at the end of your `urls.py`:

::

   import gitology.d.urls
   urlpatterns += gitology.d.urls.urlpatterns

3. add `gitology.d.middleware.GitologyMiddleware` to your `MIDDLEWARE_CLASSES`
   in `settings.py`. 

#. add the following in `settings.py` so that django can read templates stored
   in gitology repository:

::

   from gitology import settings as gsettings
   TEMPLATE_FOLDERS = (gsettings.LOCAL_REPO_PATH.joinpath("templates"), )


You will also have to tell `gitology.d` about the `.gitologyrc` configuration file. This can be achieved by setting `GITOLOGY_CONFIG_FILE` environment variable before importing `gitlogy.d` modules. 

`GITOLOGY_CONFIG_FILE` environment variable can be set in `modpython` projects by adding a `SetEnv GITOLOGY_CONFIG_FILE /location/of/gitologyrc` in apache's httpd.conf. Another way to achieve the same could be to programatically set environment variable in `settings.py` eg, inside `settings.py`::

	import os
	os.environ["GITOLOGY_CONFIG_FILE"] = "/path/of/gitlogyrc"

installation
------------

Gitology is composed of gitology-core and gitology.d, a django application. 

Gitology core consists of a set of command line scripts to work with gitology
repositories, and a django app to expose the repo on web.

**gitology core dependencies**

#. Python 2.4 or above
#. Django 1.0 or above.
#. git

**gitololgy.d, django app dependencies**

#. gitology core
#. python-yadis
#. python-openid 2.2.1 or above
#. django-openid [branch=openid-2.0+auth]
#. docutils

**installing dependencies on ubuntu**

*installing django*

First confirm that you don't have old version of django installed.

::

    $ python
    >>> import django
    >>> django
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    ImportError: No module named django
    >>> 

If you don't get the above exceptiom, you may have some django installed. Check its version:

::

    $ python
    >>> import django
    >>> django.VERSION
    >>> django.VERSION
    (1, 0, 'final')
    >>> 

Django versions less than 1.0 is not supported. 

How to delete old version of django:

::

    $ python 
    >>> import django
    >>> django
    <module 'django' from '/home/amitu/Projects/Django/django/__init__.pyc'>
    >>> raise SystemExit
    $ rm -rf $(the folder that contains old django). 

Get new django:

::

    $ wget http://www.djangoproject.com/download/1.0.2/tarball/
    $ tar -xzf Django-1.0.2-final.tar.gz
    $ cd Django-1.0.2-final
    $ sudo python setup.py install

*installing python-yadis*

::

    $ sudo easy_install python-yadis

If you get an error saying command not found for easy_install, install 
setuptools first:

::

    $ sudo apt-get install python-setuptools

*installing python-openid 2.2.1*

::

    $ wget http://openidenabled.com/files/python-openid/packages/python-openid-2.2.1.tar.gz
    $ tar -xzf python-openid-2.2.1.tar.gz
    $ cd python-openid-2.2.1
    $ sudo python setup.py install 

*installing django-openid*

::

    $ svn checkout http://django-openid.googlecode.com/svn/branches/openid-2.0+auth/django_openidconsumer

Because django-openid does not come with an installation method as yet, you
will have to manually copy it on of the folders in python's path. To get the
system folders on python path, do the following:

::

    $ python
    >>> import sys
    >>> print sys.path

It will list a directories, copy django_openidconsumer in any of the
directories there.

*Installind docutils*

::

    $ sudo apt-get install python-docutils


**installing gitology**

:: 

    $ git clone http://repo.or.cz/r/gitology.git
    $ cd gitology

*To test gitology before installing, do the following*

:: 

    $ python setup.py test
    $ sudo python setup.py install

*To test gitology works*

::

    $ gitology --version
    0.1
    $ 

