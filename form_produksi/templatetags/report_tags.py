from django import template
register = template.Library()

@register.filter
def to_percent(obj, sigdigits):
    if isinstance(obj, (int, float, complex)):
        return "{0:.{sigdigits}%}".format(obj, sigdigits=sigdigits)
    else: return obj    
