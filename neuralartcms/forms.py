from django.forms import ModelForm
from django import forms
from django.forms import Form
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

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

