from django.forms import ModelForm
from django import forms
from django.forms import Form
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.files.images import get_image_dimensions

from datetime import datetime, timedelta, timezone
from neuralartcms.models import Material, Result

import json


class MaterialForm(ModelForm):
    """
    Materialのフォーム
    """
    class Meta:
        model = Material
        fields = ('user', 'material_name',
                  'style_image', 'style_segmap', 'content_image', 'content_segmap',
                  'parameters', 'start_at',)
        exclude = ('user', 'parameters',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.MAX_W = 1500
        self.MAX_H = 1500
        super(MaterialForm, self).__init__(*args, **kwargs)

    def clean_material_name(self):
        cleaned_data = super(ModelForm, self).clean()
        material_name = cleaned_data.get('material_name')

        if self.user.materials.filter(material_name=material_name).exclude(id=self.instance.pk).exists():
            # 既に、同名のMaterial nameが存在するとき
            raise forms.ValidationError('この素材名は既に存在します')

        return material_name

    def clean_style_image(self):
        style_image = self.cleaned_data["style_image"]
        w, h = get_image_dimensions(style_image)
        if w > self.MAX_W or h > self.MAX_H:
            # 画像サイズが大きすぎるとき
            raise forms.ValidationError("画像サイズは最大{}px×{}pxです。".format(self.MAX_W, self.MAX_H))
        return style_image

    def clean_content_image(self):
        content_image = self.cleaned_data["content_image"]
        w, h = get_image_dimensions(content_image)
        if w > self.MAX_W or h > self.MAX_H:
            # 画像サイズが大きすぎるとき
            raise forms.ValidationError("画像サイズは最大{}px×{}pxです。".format(self.MAX_W, self.MAX_H))
        return content_image

    def clean_start_at(self):
        cleaned_data = super(ModelForm, self).clean()
        materials = Material.objects.all()
        start_at = cleaned_data.get('start_at')
        JST = timezone(timedelta(hours=+9))

        print(type(start_at))

        if start_at <= datetime.now(JST)+timedelta(hours=3):
            # 現在より3時間後から予約可能
            error_message = "現在より3時間後から予約可能です"
            raise forms.ValidationError(error_message)

        if materials.filter(start_at=start_at).exclude(id=self.instance.pk).exists():
            # 既に同じ時間で予約がされていた場合
            error_message = "開始時間 {} は予約済みです".format(start_at)
            raise forms.ValidationError(error_message)

        return start_at

    def clean(self):
        """
        全体のバリデーション
        :return:
        """
        cleaned_data = super(ModelForm, self).clean()
        if self.is_valid:
            # 他のバリデーションが通ってない場合は、中断
            return cleaned_data

        si_w, si_h = get_image_dimensions(cleaned_data.get("style_image"))
        ss_w, ss_h = get_image_dimensions(cleaned_data.get("style_segmap"))
        ci_w, ci_h = get_image_dimensions(cleaned_data.get("content_image"))
        cs_w, cs_h = get_image_dimensions(cleaned_data.get("content_segmap"))

        if si_w != ss_w or si_h != ss_h:
            # sytle_imageとstyle_segmapのサイズが違うとき
            error_message = "Style imageとStyle segmapのサイズが違います"
            self._errors["style_image"] = self.error_class(["size: {}×{}".format(si_w, si_h)])
            self._errors["style_segmap"] = self.error_class(["size: {}×{}".format(ss_w, ss_h)])
            raise forms.ValidationError(error_message)

        if ci_w != cs_w or ci_h != cs_h:
            # content_imageとcontent_segmapのサイズが違うとき
            error_message = "Content imageとContent segmapのサイズが違います"
            self._errors["content_image"] = self.error_class(["size: {}×{}".format(ci_w, ci_h)])
            self._errors["content_segmap"] = self.error_class(["size: {}×{}".format(cs_w, cs_h)])
            raise forms.ValidationError(error_message)

        return cleaned_data


class MaterialParameterSetForm(Form):

    content_weight = forms.ChoiceField(
        label="コンテンツ画像の強さ",
        choices=(
            ("5e1", "強め"),
            ("5e0", "普通"),
            ("1e0", "弱め"),
        ),
    )

    style_weight = forms.ChoiceField(
        label="スタイル画像の強さ",
        choices=(
            ("1e3", "強め"),
            ("1e2", "普通"),
            ("1e0", "弱め"),
        ),
    )

    def __init__(self, *args, **kwargs):

        self.material = kwargs.pop('material')  # viewから値を受け取る
        super(MaterialParameterSetForm, self).__init__(*args, **kwargs)

        # 登録されている値を初期値として設定
        parameters = json.loads(self.material.parameters)
        self.fields["content_weight"].initial = parameters["content_weight"]
        self.fields["style_weight"].initial = parameters["style_weight"]

