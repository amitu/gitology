========
gitology
========

Note
----

This is RestructuredText_ document, and it can be viewed by using package 
restview_ (Command to use: "``$ restview .``", to install: 
"``sudo easy_install restview``"). 

Development Note
----------------

Use ``python setup.py develop`` to install instead of usual 
``python setup.py install``. 

git+openid based wiki/blog/photo-album
---------------------------------------

git file structure: 
    /blocked-authors.txt contains openid of each blocked 
    commenter/rater whatever.

    /editors.txt: these ppl can do anything. [openids]

versioned-document, type: 
    these pages are maintained in git.
    each page is identified as a folder:
    /document/some-name/ [somename is unique]
    index: index.html/index.rst
    summary: summary.html/summary.rst
    meta.json?

    #. tags: tag1, tag2 [this is the master list]
    #. title:
    #. title-slug: 
    #. container: blog@/some/date/ or wiki@label or 
       album or photo@albumname
    #. is_private

    dependencies: 
        /document/some-name/file.gif etc

    comment: 
        /document/some-name/comment/1.rst, 1.meta. comments are 
        threaded: /1.comment, /1/1.comment, 1/2.comment, 
        1/1/1.comment, comments are rated. 
        x.meta: author, timestamp, ratings: [(rater, rating), ], flagged etc.

blog, link-blog:
    /blog/year/month/date.list: containing document names timestamp and document name pairs.
    /blog/label/python.txt: containing document names. [this file is auto generated]. 

wiki:
    /wiki/some-name.txt. containing: /document/some-name/
    /wiki/mysql/insert/: containing: /document/mysql@insert/

photos:
    /photos/album.txt: 
        all photos belong to albums.
        album and photos are both documents, in album, index.html is 
        generated manually, and it contains a file: photos.txt containing 
        /document/photo-name/

cheatsheets/keynote:
    /notes/name.txt
    /notes/name/something.txt
    /notes/name/something-else.txt

tools:
------
* gitology init 
* gitology start document_name. creates a new document. 
* gitology grep, ls, cd, find [coz documents may be organized in subdirs]
* gitology blog document_name: blogs the given document. 
* gitology link url tag1, tag2: takes description on stdin.
* gitology sync: updated blog labels file, and other files as needed.
* gitology wiki document_name: creates wiki link for a document. 
* gitology create-album: creates a new album.
* gitology add-photo photo, album: adds the photo to the specified album. 
  [photo can either photo.gif or a document name].

implementation details:
-----------------------

gitology shud be a easy_install-able app, and will provide:
* command line tools
* django apps: gitology_blog, gitology_wiki, gitology_album and so on.

gitology can be installed system wide and users can configure it as per 
their preferences. preferences are stored in ~/.gitologyrc. 

on preferences:
    ideally a user shud be able to work with more than on gitology 
    instances, selectable based on env variable, if more than one 
    instances exist. 
    
    export GITOLOGY_CONFIG_FILE=".filenamerc"

    .gitologyrc config file. 

    configuration:

    * repo-path: where git repo is located
    * remote: remote where git shud push after commits if required. 

there is a lib. import gitology. it handles config parsing. it handles 
reading and writing documents. it handles blog, comments, wiki, etc. and
it handles versioning.

gitology.document.Document is the document abstraction. 

Basic info:
    Document.index_content, Document.index_name, Document.index_raw, 
    Document.summary_content, Document.summary_name, Document.summary_raw, 
    Document.meta.title, Document.meta.title_slug, Document.meta.tags, 
    Document.meta.container, Document.meta.is_private.

dependency handling:
    Document.deps: key==filename, content==content of file, url, mime_type

comments:
    Document.replies: list of Comment. Comment.title, Comment.content, 
    Comment.content_raw, Comment.openid, Comment.poster_name, 
    Comment.poster_email, Comment.poster_url, Comment.posted_on
    Comment.ratings: array of (openid, rating). Comment.score, 
    Comment.replies. Comment.versions [CommentRevision(ts, content, title)]

Versioning:
    Document.versions: [DocumentRevision(ts, title, content)]

methods:
    * Document.update_title(title)
    * Document.update_content(content, type=rst) => changing type raises exception.
    * Document.add_comment(author, content, title=None, in_reply_to=None, timestamp=None)

gitology.blog.Post:
    Post.document, Post.title, Post.posted_on, Post.slug, Post.content
    Post.make_private(), Post.make_public()

gitology.blog:
    * blog_document(Document, published_on=None)
    * get_post_by_slug(slug)
    * get_posts(year=None, month=None, day=None, count=10, start=0)
    * get_post_count(year=None, month=None, day=None)

gitolog.wiki.Page:
    Page.document, Page.name, Page.content

gitology.wiki:
    * wiki_this_document(Document, published_on=None)
    * get_page_by_name(name)
    * page_exists(name)

gitology.notes.Note:
    * Note.children[ordereddict], Note.title, Note.content.

gitology.notes:
    * get_note_by_path("/mysql/insert/")
    * get_children("path", span_tree=False) :: path can be "" or "/" to indicate root.

sample filestructure:
---------------------

::

   ./wiki
   ./wiki/python.txt
   ./blocked-authors.txt
   ./editors.txt
   ./documents
   ./documents/23
   ./documents/23/ee
   ./documents/23/ee/python
   ./documents/23/ee/python/index.rst
   ./documents/23/ee/python/comments
   ./documents/23/ee/python/comments/1.rst
   ./documents/23/ee/python/comments/1.meta
   ./documents/23/ee/python/meta.json
   ./notebooks
   ./notebooks/work
   ./notebooks/personal
   ./notebooks/personal/swideas.txt
   ./notebooks/personal/swideas
   ./albums
   ./albums/lonawala.txt
   ./blogs
   ./blogs/link
   ./blogs/main
   ./blogs/main/labels
   ./blogs/main/labels/python.lst
   ./blogs/main/2008
   ./blogs/main/2008/07
   ./blogs/main/2008/07/08.lst

.. _RestructuredText: 
   http://docutils.sourceforge.net/docs/user/rst/quickref.html
.. _restview: http://mg.pov.lt/restview/
