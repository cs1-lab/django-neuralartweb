from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404

from .models import Material, Result
from .forms import MaterialForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# Materialに関する設定


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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

# ===Resultに関するView===

class ResultIndexView(ListView):
    """
    Materialに関するResultの一覧表示
    """
    template_name = "neuralartcms/result/index.html"
    context_object_name = "result_list"

    def get_queryset(self):
        material = Material.objects.filter(user=self.request.user, id=self.kwargs["material_id"])
        if not(material.count() > 0):
            # ログイン中のユーザが持つmaterialが存在しないとき
            raise Http404
        result_list = material[0].results.all().order_by("id")
        return result_list

    def get_context_data(self, **kwargs):
        context = super(ResultIndexView, self).get_context_data(**kwargs)
        # urlからmaterialを取得
        material = Material.objects.get(id=self.kwargs["material_id"])
        context["material"] = material
        return context

