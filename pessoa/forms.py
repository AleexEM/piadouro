from django.forms import ModelForm, inlineformset_factory, CharField, PasswordInput, Select
from django.contrib.auth.models import User
from pessoa.models import Perfil

class UserForm(ModelForm):
    password2 = CharField(max_length=60, required=True, widget=PasswordInput())

    class Meta:
        model = User
        exclude = [
            'is_staff',
            'is_active',
            'date_joined',
            'last_login',
            'groups',
            'user_permissions',
            'is_superuser',
        ]
        widgets = {
            'password': PasswordInput()
        }


class UserEditorForm(ModelForm):
    class Meta:
        model = User
        exclude = [
            'is_staff',
            'is_active',
            'date_joined',
            'last_login',
            'groups',
            'user_permissions',
            'is_superuser',
            'password',
        ]

class UserProfileForm(ModelForm):
    class Meta:
        model = Perfil
        exclude = ['usuario', 'seguindo']
