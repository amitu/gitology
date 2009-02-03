from django import template
import md5

from gitology.utils import parse_date

register = template.Library()

@register.filter(name="md5")
def md5sum(s):
    return md5.new(s).hexdigest()

@register.filter
def ts2date(s):
    return parse_date(s)

@register.inclusion_tag('comments.html', takes_context=True)
def show_comments(context, document):
    return { 'document': document, 'form': context['form'] } 
