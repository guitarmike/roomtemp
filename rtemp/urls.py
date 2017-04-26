from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?P<room_id>[0-9]+)/$', views.detail, name='detail'),
    url('^accounts/', include('django.contrib.auth.urls')),
]
