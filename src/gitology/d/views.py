from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required

def show_blog(request, name): 
    return render_to_response(
        "blog/index.html",
        { 'name': name },
        context_instance = RequestContext(request)
    )
def show_post(request, blog_name, post_slug): pass
def show_archive(request, blog_name, archive_format): pass
def show_category(request, blog_name, category_slug): pass
def show_wiki(request, page): pass
def add_comment(request, document_name): pass
def index(request): return HttpResponse("OK")
