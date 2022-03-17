from django import template

register = template.Library()


@register.filter(name="cut_text")
def cut_text(description, length):
    return description[:length]
