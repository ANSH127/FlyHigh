from django import template

register=template.Library()
@register.filter(name='date_format')
def date_format(val):
    val=str(val)
    return val[:5]
    
