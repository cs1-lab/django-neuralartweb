from django.conf.urls import url
from django.urls import path

from rest_framework import routers
from .views import MaterialDetailListAPIView, ResultSetView

router = routers.DefaultRouter()

urlpatterns = [
    path('material_detail/<int:year>/<int:month>/<int:day>/<int:hour>',
         MaterialDetailListAPIView.as_view(), name='material_detail'),
    path('result_set/<int:material_id>', ResultSetView.as_view(), name='result_set'),
]

urlpatterns += router.urls
