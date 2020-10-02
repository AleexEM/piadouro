from django import template

from piado.models import Piado

register = template.Library()

@register.filter
def already_repiado(user, piado):
    return Piado.objects.filter(proprietario=user, repiado_hospedeiro=piado).exists()


@register.filter
def already_like(user, piado):
    return Piado.objects.filter(id=piado.id, curtidas__in=[user]).exists()
