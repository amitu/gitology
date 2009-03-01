# imports # {{{
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list
from django.conf import settings 

import sys

import threading # theme is passed thru thread local

from gitology.config import settings as gsettings
from gitology import utils
from gitology.document import Document
from gitology.d import forms
from gitology.d.utils import select_theme

gsettings.threadlocal = threading.local()
# TODO find out exactly why its considered a hacky solution
# }}}

# blog related views # {{{
# show_blog # {{{
@select_theme
def show_blog(request, blog_data): 
    return object_list(
        request, queryset = blog_data["posts"],
        template_name = loader.select_template(
            ["blog/%s/index.html" % blog_data["name"], "blog/index.html"]
        ).name,
        template_object_name = "post", paginate_by = 10, 
        extra_context = { 'blog_data': blog_data },
    )
# }}}

# show_category # {{{
@select_theme
def show_category(request, blog_data, label_name): 
    try:
        category_data = blog_data["labels"][label_name]
    except KeyError: raise Http404
    return object_list(
        request, queryset = category_data["posts"],
        template_name = loader.select_template(
            ["blog/%s/category.html" % blog_data["name"], "blog/category.html"]
        ).name,
        template_object_name = "post", paginate_by = 10,
        extra_context = { 
            'blog_data': blog_data, 'category_data': category_data 
        },
    )
# }}}

# show_post # {{{
@select_theme
def show_post(request): 
    blog_data = utils.global_blog_dict[request.path]
    post = blog_data["posts"][request.path]
    remote_ip = request.META['REMOTE_ADDR']
    if request.method == "POST":
        form = forms.CommentForm(request, remote_ip, request.POST)
        if form.is_valid():
            chash = "#comment%s" % form.save(post["document"]).gid()
            return HttpResponseRedirect(request.path + chash)
    else:
        form = forms.CommentForm(request, remote_ip)
    return render_to_response(
        ["blog/%s/post.html" % blog_data["name"], "blog/post.html", ],
        { 'blog_data': blog_data, 'post': post, 'form': form },
        context_instance = RequestContext(request)
    )
# }}}

def show_archive(request, blog_name, archive_format): pass
# }}}

# wiki related views # {{{
# show_wiki # {{{
@select_theme
def show_wiki(request): 
    document = utils.global_wiki_dict[request.path] 
    if document.meta.get("private"):
        if not unicode(request.openid) in (
            document.meta.get(
                "viewers", []
            ) + gsettings.LOCAL_REPO_PATH.joinpath(
                "editors.txt"
            ).read().split()
        ):
            raise Http404
    remote_ip = request.META['REMOTE_ADDR']
    if request.method == "POST":
        form = forms.CommentForm(request, remote_ip, request.POST)
        if form.is_valid():
            chash = "#comment%s" % form.save(document).gid()
            return HttpResponseRedirect(request.path + chash)
    else:
        form = forms.CommentForm(request, remote_ip)
    return render_to_response(
        [
            document.meta.get("template", "non_existant"),
            "wiki/page.html"
        ], 
        { 'document': document, 'form': form },
        context_instance = RequestContext(request)
    )
# }}}
def add_comment(request, document_name): pass
def index(request): return HttpResponse("OK")
# }}}

@select_theme
def show_document(request, name):
    if not settings.LOCAL_INSTANCE: raise Http404
    document = Document(name)
    if not document.exists(): raise Http404
    return render_to_response(
        "document.html", { 'document': document },
        context_instance=RequestContext(request),
    )
