from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Material関連
    path('material/', views.MaterialIndexView.as_view(), name='material_index'),  # 一覧
    path('material/add/', views.MaterialCreateView.as_view(), name='material_add'),  # 新規登録
    path('material/<int:pk>/delete', views.MaterialDeleteView.as_view(), name='material_delete'),  # 削除
    path('material/<int:material_id>/parameterset', views.MaterialParameterSetView.as_view(),
         name="material_parameterset"),  # parameter設定
    # Result関連
    path('result/<int:material_id>/', views.ResultIndexView.as_view(), name='result_index'),  # 一覧
]
