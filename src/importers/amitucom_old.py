from django.utils import simplejson

from gitology.document import Document
from gitology.blog import blog_document

blog = "main"
author = "Amit Upadhyay"

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

def parse_date(s):
    from django.db.models.fields import DateTimeField
    dtf = DateTimeField()
    return dtf.to_python(s)

MONTHS = {
    1:'january', 2:'february', 3:'march', 4:'april', 5:'may', 6:'june',
    7:'july', 8:'august', 9:'september', 10:'october', 11:'november',
    12:'december'
}

def get_post_url(p):
    posted_on = parse_date(p["fields"]["posted_on"])
    return "/blog/%2d/%s/%s" % (
        posted_on.year, MONTHS[posted_on.month],
        p[u'fields']['title_slug']
    )

def convert_to_document_name(u):
    return u[1:].replace("/", "@")

def create_post(post, data):
    post_url = get_post_url(post)
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
    document.meta.save()
    blog_document(document, post_url, blog, posted_on)
    print post_url, post_name, post_title

def main():
    d = collect_data()
    for post in d[u"blog.post"]:
        create_post(post, d)
    
if __name__ == "__main__":
    main()
