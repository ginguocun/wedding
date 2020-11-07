from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
]


if settings.STATIC_ROOT and settings.STATIC_URL:
    urlpatterns.append(re_path(
        r'^{0}(?P<path>.*)$'.format(settings.STATIC_URL[1:]),
        serve, {'document_root': settings.STATIC_ROOT}, name='static'))
