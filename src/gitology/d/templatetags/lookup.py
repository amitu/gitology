from django import template

register = template.Library()

@register.filter
def lookup(k, v):
    return k[v]
