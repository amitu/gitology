# imports # {{{
from gitology.config import settings as gsettings
from gitology.document import Document

from datetime import datetime
# }}}

# create_blog # {{{
def create_blog(blog, author, title, subtitle):
    document = Document("blogs@%" % blog)
    if not document.exists():
        document.create(
            index_content = title,
            format = "html", author = author,
        )
    else:
        document.set_raw_index(title, "html")
    document.meta.author = author
    document.meta.title = title
    document.meta.subtitle = subtitle
    document.meta.url = "/%s/" % blog
    document.meta.type = "blog"
    document.meta.save()

    # create blog folder
    blog_folder = gsettings.LOCAL_REPO_PATH.joinpath("blogs/%s" % blog)
    if not blog_folder.exists(): blog_folder.makedirs()

    labels_folder = gsettings.LOCAL_REPO_PATH.joinpath("blogs/%s/labels" % blog)
    if not labels_folder.exists(): labels_folder.makedirs()
# }}}

# create_label # {{{
def create_label(blog, author, label_name, label_slug, label_description=None):
    if label_description is None:
        label_description = label_name
    # create label document
    document = Document(
        "blogs@%s@label@%s" % (blog, label_slug)
    )
    if not document.exists():
        document.create(
            index_content = label_name,
            format = "html", author = author,
        )
    else:
            document.set_raw_index(label_name, "html")
    document.meta.author = author
    document.meta.title = label_name
    document.meta.description = label_descrption
    document.meta.slug = label_slug
    document.meta.type = "blog_label"
    document.meta.save()
# }}}

# blog_document # {{{
def blog_document(document, url, blog="main", dtime=None):
    if not dtime: dtime = datetime.now()
    blog_file = gsettings.LOCAL_REPO_PATH.joinpath(
        "blogs"
    ).joinpath(blog).joinpath("%04d" % dtime.year).joinpath(
        "%02d" % dtime.month
    ).joinpath("%02d.lst" % dtime.day)
    if not blog_file.parent.exists(): 
        blog_file.parent.makedirs()
    blog_file.open("a+").write(
        "%s %s %s\n" % (url, document.name, str(dtime))
    )
    document.meta.url = url
    document.meta.save()
    for label in document.meta.get("labels", []):
        gsettings.LOCAL_REPO_PATH.joinpath(
            "blogs/%s/labels/%s.lst" % (blog, label)
        ).open("a+").write("%s\n" % url)
# }}}
