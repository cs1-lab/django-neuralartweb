from django.db import models
from accounts.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import ResizeToFit


class Material(models.Model):
    """
    画風変換にて入力する情報
    """
    user = models.ForeignKey(User, related_name='materials', on_delete=models.CASCADE)
    material_name = models.CharField(max_length=100)

    # TODO: 幅は縮小する処理をしているが、高さに関する処理がない
    # ResizeToFillやSmartResizeを使えばよいかも。調査の必要あり。
    content_image = models.ImageField(upload_to='images/material/content/')
    content_image_xs = ImageSpecField(source='content_image',
                                             processors=[ResizeToFit(width='150')],
                                             format='JPEG',
                                             options={"quality": 60})
    content_image_sm = ImageSpecField(source='content_image',
                                         processors=[ResizeToFit(width='500', upscale=False)],
                                         format='JPEG',)

    content_segmap = models.ImageField(upload_to='images/material/content_segmap')
    content_segmap_xs = ImageSpecField(source='content_segmap',
                                              processors=[ResizeToFit(width='150')],
                                              format='JPEG',
                                              options={"quality": 60})
    content_segmap_sm = ImageSpecField(source='content_segmap',
                                          processors=[ResizeToFit(width='500', upscale=False)],
                                          format='JPEG',)

    style_image = models.ImageField(upload_to='images/material/style/')
    style_image_xs = ImageSpecField(source='style_image',
                                           processors=[ResizeToFit(width='150')],
                                           format='JPEG',
                                           options={"quality": 60})
    style_image_sm = ImageSpecField(source='style_image',
                                       processors=[ResizeToFit(width='500', upscale=False)],
                                       format='JPEG',)

    style_segmap = models.ImageField(upload_to='images/material/style_segmap')
    style_segmap_xs = ImageSpecField(source='style_segmap',
                                            processors=[ResizeToFit(width='150')],
                                            format='JPEG',
                                            options={"quality": 60})
    style_segmap_sm = ImageSpecField(source='style_segmap',
                                        processors=[ResizeToFit(width='500', upscale=False)],
                                        format='JPEG',)

    parameters = models.TextField(blank=True)  # パラメータ調整値、Jsonで格納すること
    start_at = models.DateTimeField(blank=True)
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
