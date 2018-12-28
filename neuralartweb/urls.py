"""neuralartweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from neuralartcms import views

urlpatterns = [
    path('', views.home, name="top"),  # トップページ
    path('cms/', include(('neuralartcms.urls', 'cms'),)),
    # ログイン関連ビュー
    path('accounts/', include(('accounts.urls', 'accounts'),)),
    path('admin/', admin.site.urls),
    # api v0
    path('api_v0/', include(('api_v0.urls', 'api_v0'),)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
