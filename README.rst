========
gitology
========

git+openid based wiki/blog/photo-album
---------------------------------------

git file structure: 
    /blocked-authors.txt contains openid of each blocked commenter/rater whatever.

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
    #. container: blog@/some/date/ or wiki@label or album or photo@albumname
    #. is_private

    dependencies: 
        /document/some-name/file.gif etc

    comment: 
        /document/some-name/comment/1.rst, 1.meta. comments are threaded: /1.comment, /1/1.comment, 1/2.comment, 1/1/1.comment, comments are rated. 
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
        album and photos are both documents, in album, index.html is generated manually, and it contains a file: photos.txt containing /document/photo-name/

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
* gitology add-photo photo, album: adds the photo to the specified album. [photo can either photo.gif or a document name].

implementation details:
-----------------------

gitology shud be a easy_install-able app, and will provide:
* command line tools
* django apps: gitology_blog, gitology_wiki, gitology_album and so on.

gitology can be installed system wide and users can configure it as per their preferences. preferences are stored in ~/.gitologyrc. 

on preferences:
    ideally a user shud be able to work with more than on gitology instances, selectable based on env variable, if more than one instances exist. 
    
    export GITOLOGY_CONFIG_FILE=".filenamerc"

    .gitologyrc config file. 

    configuration:

    * repo-path: where git repo is located
    * remote: remote where git shud push after commits if required. 

there is a lib. import gitology. it handles config parsing. it handles reading and writing documents. it handles blog, comments, wiki, etc. 
