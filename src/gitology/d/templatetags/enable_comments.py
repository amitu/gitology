from django import template

register = template.Library()

@register.inclusion_tag('comments.html', takes_context=True)
def show_comments(context, document):
    return { 'document': document, 'form': context['form'] } 
