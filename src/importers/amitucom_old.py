# imports and settings # {{{
from django.utils import simplejson

from gitology.document import Document
from gitology.blog import blog_document
from gitology.config import settings as gsettings

blog = "main"
author = "Amit Upadhyay"
# }}}

# collect_data # {{{
def collect_data():
    data = simplejson.load(file("amitucom/amitucom.blog.json"))
    categories = {}
    blogs = {}
    posts = []
    d = { u'blog.category': categories, u'blog.blog': blogs, u'blog.post': posts }
    for i in data:
        if i[u'model'] == u'blog.post':
            d[i[u'model']].append(i)
        else:
            d[i[u'model']][i[u'pk']] = i[u'fields']
    return d
# }}}

# parse_date # {{{
def parse_date(s):
    from django.db.models.fields import DateTimeField
    dtf = DateTimeField()
    return dtf.to_python(s)
# }}}

# MONTHS # {{{
MONTHS = {
    1:'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june',
    7:'july', 8:'august', 9:'september', 10:'october', 11:'november',
    12:'december'
}
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

# create_label # {{{
def create_label(label_id, label_data, blog_data):
    # create label document
    document = Document(
        "blogs@main@label@%s" % label_data["name_slug"]
    )
    if not document.exists():
        document.create(
            index_content = label_data["name"],
            format = "html", author = author,
        )
    else:
            document.set_raw_index(label_data["name"], "html")
    document.meta.author = author
    document.meta.title = label_data["name"]
    document.meta.description = label_data["descrption"]
    document.meta.slug = label_data["name_slug"]
    document.meta.type = "blog_label"
    document.meta.label_id = label_id
    document.meta.save()
# }}}

# main # {{{
def main():
    d = collect_data() # read data from json file

    # create blog
    document = Document("blogs@main")
    if not document.exists():
        document.create(
            index_content = "A blog by Amit Upadhyay",
            format = "html", author = author,
        )
    else:
        document.set_raw_index("A blog by Amit Upadhyay", "html")
    document.meta.author = author
    document.meta.title = "Anything Else"
    document.meta.subtitle = "Nerdier than thou"
    document.meta.url = "/blog/"
    document.meta.type = "blog"
    document.meta.save()

    # create blog folder
    blog_folder = gsettings.LOCAL_REPO_PATH.joinpath("blogs/main")
    if not blog_folder.exists(): blog_folder.makedirs()

    labels_folder = gsettings.LOCAL_REPO_PATH.joinpath("blogs/main/labels")
    if not labels_folder.exists(): labels_folder.makedirs()
    
    for label_id, label_data in d["blog.category"].items():
        create_label(label_id, label_data, d)

    for post in d[u"blog.post"]:
        create_post(post, d)
    print "imported", len(d["blog.post"]), "posts"
# }}}

if __name__ == "__main__": main()
