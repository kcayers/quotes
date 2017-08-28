from django.conf.urls import url
from . import views

urlpatterns = [
     url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.home),
    url(r'^create$', views.create),
    url(r'^user/(?P<user_id>\d+)$', views.show_user),
    url(r'^add/(?P<quote_id>\d+)$',views.add),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove),
    url(r'^logout$', views.logout),
]
