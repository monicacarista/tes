from django.template import Library

register = Library()

@register.filter
def keyvalue(dict, key):    
    return dict[key]