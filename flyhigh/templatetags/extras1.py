from django import template

register=template.Library()
@register.filter(name='max_price')



def max_price(val,item):
    x=0
    if val=='Economy':
        
        for i in item:
             if i.economy_fare>x:
                x=i.economy_fare

    if val=='Business':
        for i in item:
             if i.business_fare>x:
                x=i.business_fare
    if val=='First Class':
        for i in item:
             if i.first_fare>x:
                x=i.first_fare
    
    print(x)
    return x