from django.conf import settings  ##新增
from django.contrib import admin
from django.urls import path
from django.urls import re_path as url
from django.urls.conf import include, re_path
from django.views import static
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("app.urls")),

    # 静态资源路径
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
