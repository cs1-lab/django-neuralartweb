from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.decorators import detail_route, action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from django.core import exceptions
from django.contrib.auth import get_user_model

from neuralartcms.models import Material, Result
from .serializer import MaterialDetailSerializer, ResultSetSerializer
from datetime import datetime, timezone, timedelta


class MaterialDetailListAPIView(ListAPIView):
    """
    materialの詳細情報を返す

    問い合わせ例
    -------------
    ex: 2018年12月12日 18:00の詳細情報を取得::

        /material_detail/2018/12/12/18
    """
    queryset = Material.objects.all()
    serializer_class = MaterialDetailSerializer
    http_method_names = ['get', ]  # getしか受け付けない

    authentication_classes = ()
    permission_classes = ()

    def __init__(self, *args, **kwargs):
        super(MaterialDetailListAPIView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        hour = self.kwargs["hour"]
        JST = timezone(timedelta(hours=+9))

        start_at_ = datetime(year, month, day, hour, 0, 0, tzinfo=JST)

        materials = Material.objects.filter(start_at=start_at_)

        return materials


class ResultSetView(ListCreateAPIView):
    """
    result登録用

    問い合わせ例: (POST)
    ---------------------


    """
    serializer_class = ResultSetSerializer
    queryset = Result.objects.all()

    authentication_classes = ()
    permission_classes = ()

    def get_serializer_context(self):
        context = {}  # serializerに渡す値
        materials = Material.objects.all()
        material_id = self.kwargs["material_id"]

        # TODO: ここにバリデーションみたいな処理を書いていいかは気になる
        # serializerに書くべきでは?
        if materials.filter(id=material_id).exists():
            # materialが存在したとき
            context["material"] = materials.get(id=material_id)
        else:
            # materialが存在しないとき
            context["material"] = False

        return context
