# imports and settings # {{{
try:
    import pydelicious
except ImportError:
    print "pydelicious module requried."
    print "Get it from http://code.google.com/p/pydelicious/." 
    raise SystemExit    

from gitology.document import Document
from gitology.blog import blog_document, create_blog, create_label
from gitology.config import settings as gsettings
from gitology.utils import parse_date

import pickle

import getpass

blog = "links"
author = "Amit Upadhyay"
title = "Amit Upadhyay's Link Blog"
subtitle = "Amit Upadhyay's Link Blog"
# }}}

# collect_data # {{{
def collect_data():
    labels = set()
    posts = []
    for post in pydelicious.get_all("upadhyay", "2muchluv")["posts"]:
        posts.append(post)
        labels = labels.union(post["tag"].split())
    d = { 'labels': labels, 'posts': posts }
    return d
# }}}

# get_post_url # {{{
def get_post_url(p):
    posted_on = parse_date(p["fields"]["posted_on"])
    post_url = "/blog/%2d/%s/%s" % (
        posted_on.year, MONTHS[posted_on.month],
        p[u'fields']['title_slug']
    )
    if "." not in p[u'fields']['title_slug']:
        post_url += "/"
    return post_url
# }}}

# convert_to_document_name # {{{
def convert_to_document_name(u):
    if u.endswith("/"): u = u[:-1]
    return u[1:].replace("/", "@")
# }}}

# create_post # {{{
def create_post(post, data):
    post_url = get_post_url(post)
    if post_url == '/blog/2006/may/worried-sick.html': print "XXXXXXXXX"
    posted_on = parse_date(post["fields"]["posted_on"])
    post_name = convert_to_document_name(post_url)
    post_title = post[u"fields"]["title"]
    document = Document(post_name)
    if not document.exists(): 
        document.create(
            index_content = post[u'fields']["content"],
            format = "html", author = author, 
        )
    else:
        document.set_raw_index(post[u'fields']['content'], 'html')
    document.meta.author = author
    document.meta.title = post_title
    document.meta.url = post_url
    document.meta.type = "blog_post"
    document.meta.title_slug = post['fields']['title_slug']
    document.meta.posted_on = post['fields']['posted_on']
    for label_id in post['fields']['categories']:
        label_name = data["blog.category"][str(label_id)]["name_slug"]
        document.meta.setdefault("labels", []).append(label_name)
        gsettings.LOCAL_REPO_PATH.joinpath(
            "blogs/main/labels/%s.lst" % label_name
        ).open("a+").write("%s\n" % post_url)
    document.meta.save()
    blog_document(document, post_url, blog, posted_on)
# }}}

# main # {{{
def main():
    d = collect_data() # read data from delicious
    create_blog(blog, author, title, subtitle)
    for label in d["labels"]:
        create_label(blog, author, label, label)

    for post in d["posts"]:
        create_post(post, d)

    print "imported", len(d["posts"]), "posts"
# }}}

if __name__ == "__main__": main()
