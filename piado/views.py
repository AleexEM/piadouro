from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from piado.models import Piado, Hashtag
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from piadouro.mixins.page_title import PageTitleMixin
import string


class PiadoCreate(LoginRequiredMixin, CreateView):
    model = Piado
    fields = ['conteudo']

    def form_valid(self, form):
        form.instance.proprietario = self.request.user
        form.save()
        hashtags = []
        for word in form.cleaned_data['conteudo'].split(' '):
            if word.startswith('#'):
                hashtags.append(Hashtag(conteudo=word.strip(string.punctuation)))
        Hashtag.objects.bulk_create(hashtags, ignore_conflicts=True)
        form.instance.hashtags.add(*list(Hashtag.objects.filter(conteudo__in=hashtags)))
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('home'))

    def get_success_url(self):
        return reverse('home')


class PiadoDelete(LoginRequiredMixin, DeleteView):
    model = Piado
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        return self.post(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.proprietario != request.request.user:
            raise PermissionDenied
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


class PiadoLike(LoginRequiredMixin, UpdateView):
    model = Piado

    def get(self, request, *args, **kwargs):
        if request.GET.get('next_page'):
            success_url = request.GET.get('next_page')
        else:
            success_url = reverse('home')

        self.object = self.get_object()
        if self.object.curtidas.filter(id=request.user.id).exists():
            self.object.curtidas.remove(request.user.id)
        else:
            self.object.curtidas.add(request.user.id)
        return HttpResponseRedirect(success_url)


class RePiado(LoginRequiredMixin, CreateView):
    model = Piado

    def get(self, request, *args, **kwargs):
        if request.GET.get('next_page'):
            success_url = request.GET.get('next_page')
        else:
            success_url = reverse('home')

        repiado_query = Piado.objects.filter(proprietario=request.user, repiado_hospedeiro_id=kwargs['pk'])
        if repiado_query.exists():
            repiado_query.delete()
        else:
            piado_velho = get_object_or_404(Piado, id=kwargs['pk'])
            novo_piado = Piado(
                proprietario=request.user,
                conteudo=piado_velho.conteudo,
                repiado_hospedeiro=piado_velho
            )
            novo_piado.save()
        return HttpResponseRedirect(success_url)


class PiadoView(PageTitleMixin, LoginRequiredMixin, DetailView):
    model = Piado
    template_name = 'piado/detail.html'

    def get_page_title(self):
        return f'Piado de {self.object.proprietario.first_name}'

class PiadoComment(LoginRequiredMixin, CreateView):
    model = Piado
    fields = ['conteudo']

    def form_valid(self, form):
        comentario_hospedeiro = get_object_or_404(Piado, id=self.kwargs['hospedeiro'])
        form.instance.comentario_hospedeiro = comentario_hospedeiro
        form.instance.proprietario = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.request.GET.get('next_page_on_error', '/'))

    def get_success_url(self):
        return reverse('piado-detail', args=[self.kwargs['hospedeiro']])


class HashtagList(PageTitleMixin, LoginRequiredMixin, ListView):
    model = Hashtag
    template_name =  'piado/hashtags.html'
    page_title = 'Hashtags'

class HashtagPiadosList(PageTitleMixin, LoginRequiredMixin, DetailView):
    model = Hashtag
    template_name = 'home.html'

    def get_page_title(self):
        return f'Piados com #{self.kwargs["hasgtag"]}'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.model, conteuto=self.kwargs['hashtag'].lower())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['piados'] = self.object.piados.all()
        return context