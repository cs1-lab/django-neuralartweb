from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Material関連
    path('material/', views.MaterialIndexView.as_view(), name='material_index'),  # 一覧
    path('material/add/', views.MaterialCreateView.as_view(), name='material_add'),  # 新規登録
    # Result関連
    path('result/<int:material_id>/', views.ResultIndexView.as_view(), name='result_index'),  # 一覧
]
