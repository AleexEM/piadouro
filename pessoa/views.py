from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import RedirectView, TemplateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from pessoa.models import Perfil
from django.contrib.auth.mixins import LoginRequiredMixin
from pessoa.forms import UserProfileForm, UserForm, UserEditorForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from piado.models import Piado
from django.db.models import Q
from piadouro.mixins.page_title import PageTitleMixin


class Home(PageTitleMixin, LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_page_title(self):
        return f'Home de {self.request.user.first_name}'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        q = self.request.GET.get('q', False)
        if not q:
            context['piados'] = Piado.objects.filter(
                Q(proprietario=self.request.user) |
                Q(proprietario__in=self.request.user.perfil.seguindo.all())
            )
        else:
            context['piados'] = Piado.objects.filter(conteudo__icontains=q)
            context['q'] = q
        return context

class UserDetail(PageTitleMixin, LoginRequiredMixin, DetailView):
    model = User
    template_name = 'home.html'

    def get_page_title(self):
        return f'Timeline de {self.object.first_name}'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, username=self.kwargs['username'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['piados'] = Piado.objects.filter(proprietario=self.object)
        return context

class UserList(PageTitleMixin, LoginRequiredMixin, ListView):
    template_name = 'user_list.html'
    model = Perfil
    page_title = 'Lista de usuários'


class Follow(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'usuarios'

    def get_redirect_url(self, *args, **kwargs):
        user_to_follow = get_object_or_404(User, pk=kwargs['user_id'])
        if self.request.user.perfil.seguindo.filter(pk=user_to_follow.pk).exists():
            self.request.user.perfil.seguindo.remove(user_to_follow)
        else:
            self.request.user.perfil.seguindo.add(user_to_follow)
        return super().get_redirect_url()


class Registration(PageTitleMixin, CreateView):
    model = User
    template_name = 'create_user.html'
    form_class = UserForm
    page_title = 'Crie sua conta'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'action': reverse('registration'),
            'button_text': 'Cadastrar'
        })
        context['form'] = self.get_form()
        if self.request.method == 'POST':
            context['profile_form'] = UserProfileForm(self.request.POST, self.request.FILES)
        else:
            context['profile_form'] = UserProfileForm()
        return context


    def post(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data()

        if context['form'].is_valid() and context['profile_form'].is_valid():
            user = context['form'].save(commit=False)
            user.set_password(context['form'].cleaned_data['password'])
            user.save()
            context['profile_form'].instance.usuario = user
            context['profile_form'].save()
            new_user = authenticate(
                request,
                username=context['form'].cleaned_data['username'],
                password=context['form'].cleaned_data['password'],
            )
            login(request, new_user)
            return redirect('home')
        return self.render_to_response(context)

class ProfileEditor(PageTitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'create_user.html'
    form_class = UserEditorForm
    page_title = 'Editar perfil'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.request.user.id)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'action': reverse('profile-editor'),
            'button_text': 'Atualizar'
        })
        self.object = self.get_object()
        context['form'] = self.get_form()
        if self.request.method == 'POST':
            context['profile_form'] = UserProfileForm(self.request.POST, self.request.FILES, instance=self.object.perfil)
        else:
            context['profile_form'] = UserProfileForm(instance=self.object.perfil)
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data()

        if context['form'].is_valid() and context['profile_form'].is_valid():
            user = context['form'].save()
            context['profile_form'].save()
            return redirect('home')
        return self.render_to_response(context)
