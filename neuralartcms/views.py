from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.contrib import messages

from .models import Material, Result
from .forms import MaterialForm, MaterialParameterSetForm, ResultUpdateForm

import json


def home(request):
    return render(request, 'neuralartcms/home.html')

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
    success_url = reverse_lazy("cms:material_index")

    # ログインしているユーザを設定
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request,
                         "{}を追加しました".format(form.instance.material_name),
                         extra_tags="check")
        return super(MaterialCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        """
        formへの値渡し
        :return:
        """
        kwargs = super(MaterialCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@method_decorator(login_required, name='dispatch')
class MaterialDeleteView(DeleteView):
    """
    Material削除
    """
    model = Material
    success_url = reverse_lazy("cms:material_index")

    def get(self, request, *args, **kwargs):
        # 確認Viewは表示せず、ポップアップ
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        object_ = self.get_object()
        messages.success(self.request,
                         "{}の削除が完了しました".format(object_.material_name),
                         extra_tags="check")
        return super(MaterialDeleteView, self).delete(request, *args, **kwargs)


class MaterialParameterSetView(FormView):
    """
    Materialの(画像生成に必要な)パラメータを設定する

    parameterフィールドにjsonで保存する
    """
    form_class = MaterialParameterSetForm
    template_name = "neuralartcms/material/parameter_set.html"
    success_url = reverse_lazy("cms:material_index")

    def __init__(self, *args, **kwargs):
        super(MaterialParameterSetView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MaterialParameterSetView, self).get_context_data(**kwargs)
        # urlからmaterialを取得
        material = Material.objects.get(id=self.kwargs["material_id"])
        context["material"] = material
        return context

    def get_form_kwargs(self):
        """
        formへの値渡し
        :return:
        """
        kwargs = super(MaterialParameterSetView, self).get_form_kwargs()
        kwargs["material"] = Material.objects.get(id=self.kwargs["material_id"])
        return kwargs

    def form_valid(self, form):
        """
        parameterの設定を行う
        :param form:
        :return:
        """
        parameters = {}
        parameters["content_weight"] = self.request.POST.get("content_weight")
        parameters["style_weight"] = self.request.POST.get("style_weight")
        parameters = json.dumps(parameters)

        Material.objects.filter(id=self.kwargs["material_id"]).update(parameters=parameters)
        return super(MaterialParameterSetView, self).form_valid(form)




# ===Resultに関するView===


@method_decorator(login_required, name='dispatch')
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
        result_list = material[0].results.all().order_by("-created_at")
        return result_list

    def get_context_data(self, **kwargs):
        context = super(ResultIndexView, self).get_context_data(**kwargs)
        # urlからmaterialを取得
        material = Material.objects.get(id=self.kwargs["material_id"])
        context["material"] = material
        return context


@method_decorator(login_required, name='dispatch')
class ResultDeleteView(DeleteView):
    """
    Result削除
    """
    model = Result
    #success_url = reverse_lazy("cms:result_index")

    def get(self, request, *args, **kwargs):
        # 確認Viewは表示せず、ポップアップ
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        object_ = self.get_object()
        messages.success(self.request,
                         "結果の削除を１件完了しました",
                         extra_tags="check")
        return super(ResultDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        material_id = self.object.material.id
        return reverse_lazy('cms:result_index', kwargs={'material_id': material_id})


@method_decorator(login_required, name='dispatch')
class ResultUpdateView(UpdateView):
    """
    result更新
    主に、result_nameと共有の設定を行う
    """
    model = Result
    template_name = 'neuralartcms/edit.html'
    form_class = ResultUpdateForm

    # formへ値渡し
    def get_form_kwargs(self):
        kwargs = super(ResultUpdateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        material_id = self.object.material.id
        return reverse_lazy('cms:result_index', kwargs={'material_id': material_id})
