from django import template

register=template.Library()
@register.filter(name='min_price')

def min_price(val,item):
    if val=='Economy':
        x=item[0].economy_fare
        for i in item:
             if i.economy_fare<x:
                x=i.economy_fare

    if val=='Business':
        x=item[0].business_fare
        # print(x)
        for i in item:
             if i.business_fare<x:
                x=i.business_fare
    if val=='First Class':
        x=item[0].first_fare
        for i in item:
             if i.first_fare<x:
                x=i.first_fare
    
    print(x)
    return x