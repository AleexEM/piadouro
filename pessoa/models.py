from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

ESTADO_CIVIL = (
    ('s', 'Solteiro'),
    ('n', 'Namorando'),
    ('no', 'Noivado'),
    ('c', 'Casado'),
    ('v', 'Viuvo'),
    ('p', 'Piranhage'),
)

ESTADOS = (
    ('rs', 'Rio Grande do Sul'),
    ('sc', 'Santa catarina'),
    ('pr', 'Paraná'),
)

def validador_idade(data_nascimento):
    hoje = date.today()
    delta = hoje - data_nascimento

    if delta.days / 365.25 < 18:
        raise ValidationError(
            'Sai fora menó',
            params={'value': data_nascimento},
        )


class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto = models.ImageField(upload_to='piadouro/imagens/')
    telefone = models.CharField(max_length=20)
    estado_civil = models.CharField(max_length=2, choices=ESTADO_CIVIL)
    data_nascimento = models.DateField(validators=[validador_idade])
    estado = models.CharField(max_length=2, choices=ESTADOS)
    cidade = models.CharField(max_length=64)
    desempregado = models.BooleanField()

    seguindo = models.ManyToManyField(User, related_name='seguidores', symmetrical=False, blank=True)

    def __str__(self):
        return f'{self.usuario}'
