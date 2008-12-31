# imports # {{{
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list
from django.conf import settings 

import sys

from gitology.config import settings as gsettings
from gitology import utils
# }}}

# blog related views # {{{
# show_blog # {{{
def show_blog(request, blog_data): 
    return object_list(
        request, queryset = blog_data["posts"],
        template_name = "blog/index.html", 
        template_object_name = "post", paginate_by = 30, 
        extra_context = { 'blog_data': blog_data },
    )
# }}}

# show_category # {{{
def show_category(request, blog_data, label_name): 
    try:
        category_data = blog_data["labels"][label_name]
    except KeyError: raise Http404
    return object_list(
        request, queryset = category_data["posts"],
        template_name = "blog/category.html",
        template_object_name = "post", paginate_by = 30,
        extra_context = { 
            'blog_data': blog_data, 'category_data': category_data 
        },
    )
# }}}

# show_post # {{{
def show_post(request): 
    blog_data = utils.global_blog_dict[request.path]
    post = blog_data["posts"][request.path]
    return render_to_response(
        ["blog/%s/post.html" % blog_data["name"], "blog/post.html", ],
        { 'blog_data': blog_data, 'post': post },
        context_instance = RequestContext(request)
    )
# }}}

def show_archive(request, blog_name, archive_format): pass
# }}}

# wiki related views # {{{
def show_wiki(request, page): pass
def add_comment(request, document_name): pass
def index(request): return HttpResponse("OK")
# }}}
