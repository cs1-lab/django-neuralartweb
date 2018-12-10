from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .models import Material, Result
from .forms import MaterialForm

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Materialに関する設定


class MaterialIndexView(ListView):
    """
    Materialの一覧表示
    """
    template_name = 'neuralartcms/material/index.html'
    context_object_name = 'material_list'

    def get_queryset(self):
        user = self.request.user
        materials = user.materials.all()
        return materials


class MaterialCreateView(CreateView):
    """
    Material新規作成
    """
    model = Material
    template_name = 'neuralartcms/material/edit.html'
    form_class = MaterialForm
    success_url = reverse_lazy('cms:index')

    # ログインしているユーザを設定
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MaterialCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        """
        formへの値渡し
        :return:
        """
        kwargs = super(MaterialCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

