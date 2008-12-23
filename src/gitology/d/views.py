# imports # {{{
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required

import sys

from gitology.config import settings as gsettings
# }}}

# show_blog # {{{
def show_blog(request, blog_data): 
    return render_to_response(
        ["blog/%s/index.html" % blog_data["name"], "blog/index.html", ],
        { 'blog_data': blog_data },
        context_instance = RequestContext(request)
    )
# }}}

# show_category # {{{
def show_category(request, blog_data, category_data): 
    return render_to_response(
        ["blog/%s/category.html" % blog_data["name"], "blog/category.html", ],
        { 'blog_data': blog_data, 'category_data': category_data },
        context_instance = RequestContext(request)
    )
# }}}

def show_post(request, blog_name, post_slug): pass
def show_archive(request, blog_name, archive_format): pass
def show_wiki(request, page): pass
def add_comment(request, document_name): pass
def index(request): return HttpResponse("OK")
