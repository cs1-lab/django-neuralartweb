from django.db import models
from accounts.models import User


class Material(models.Model):
    """
    画風変換にて入力する情報
    """
    user = models.ForeignKey(User, related_name='results', on_delete=models.CASCADE)
    material_name = models.CharField(max_length=100)
    content_image = models.ImageField(upload_to='images/material/content/')
    content_segmap = models.ImageField(upload_to='images/material/content_segmap')
    style_image = models.ImageField(upload_to='images/material/style/')
    style_segmap = models.ImageField(upload_to='images/material/style_segmap')
    parameters = models.TextField(blank=True)  # パラメータ調整値、Jsonで格納すること
    great_result = models.CharField(max_length=100)

    def __repr__(self):
        # 主キーとnameを返して見やすくする
        # ex: 1 : material_01
        return "{}: {}".format(self.pk, self.material_name)

    __str__ = __repr__


class Result(models.Model):
    """
    画風変換による出力画像'1枚'を保持する
    """
    material = models.ForeignKey(Material, related_name='results', on_delete=models.CASCADE)
    result_image = models.ImageField(upload_to='images/result/')
    iteration = models.IntegerField()
    result_info = models.TextField(blank=True)

    def __repr__(self):
        # 主キーとカウント数を返して見やすくする
        # ex: 1 : iteration()
        return "{}: iteration({:5d})".format(self.pk, self.iteration)

    __str__ = __repr__
