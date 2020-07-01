from django import template

register = template.Library()

@register.filter(name="div")
def mydiv(value1, value2):
    if int(value2)==0:
        return "NA"
    else:
        return str(int(value1)/int(value2))


@register.filter(name="sub")
def mysub(value1, value2):

    return str(int(value1)-int(value2))

@register.filter(name="isList")
def myislist(object):

    if isinstance(object,list):
        return "list"
    else:
        return "nolist"

@register.filter(name="lenOfList")
def mylenOfList(object):

    if isinstance(object,list):
        return len(object)
    elif isinstance(object,dict):
        return 1
    else:
        return object