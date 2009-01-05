"""
    template tag library to access document attributes etc
"""
from django import template

register = template.Library()

from gitology.document import Document

@register.filter
def name_to_document(name): 
    """
    name_to_document filter takes name and returns document
    """
    return Document(name)

def get_document(name, v):
    """
    get_document template tag takes name and updates context
    """

