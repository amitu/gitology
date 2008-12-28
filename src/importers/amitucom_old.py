from django.utils import simplejson

from gitology.document import Document

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

def get_post_url(p):
    return "/blog/2007/august/%s" % p[u'fields']['title_slug']

def convert_to_document_name(u):
    return u[1:].replace("/", "@")

def create_post(post, data):
    post_url = get_post_url(post)
    post_name = convert_to_document_name(post_url)
    post_title = post[u"fields"]["title"]
    document = Document(post_name)
    if not document.exists(): 
        document.create(
            index_content = post[u'fields']["content"],
            format = "html", author = "Amit Upadhyay",
        )
    else:
        document.set_raw_index(post[u'fields']['content'], 'html')
    document.meta.author = "Amit Upadhyay"
    document.meta.title = post_title
    document.meta.url = post_url
    document.meta.type = "blog_post"
    document.meta.title_slug = post['fields']['title_slug']
    document.meta.posted_on = post['fields']['posted_on']
    document.meta.save()
    print post_url, post_name, post_title

def main():
    d = collect_data()
    for post in d[u"blog.post"]:
        create_post(post, d)
    
if __name__ == "__main__":
    main()
