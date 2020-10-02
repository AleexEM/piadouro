from django import template

register = template.Library()

@register.filter
def exists(profile, user_list):
    return user_list.filter(pk=profile.pk).count() == 1
