from django.forms import ModelForm
from django import forms
from django.forms import Form
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from datetime import datetime, timedelta, timezone
from neuralartcms.models import Material, Result


class MaterialForm(ModelForm):
    """
    Materialのフォーム
    """
    class Meta:
        model = Material
        fields = ('user', 'material_name',
                  'style_image', 'style_segmap', 'content_image', 'content_segmap',
                  'parameters', 'start_at',)
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(MaterialForm, self).__init__(*args, **kwargs)

    def clean_material_name(self):
        cleaned_data = super(ModelForm, self).clean()
        material_name = cleaned_data.get('material_name')

        if self.user.materials.filter(material_name=material_name).exclude(id=self.instance.pk).exists():
            # 既に、同名のMaterial nameが存在するとき
            raise forms.ValidationError('この素材名は既に存在します')

        return material_name

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
