from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^create', views.create, name="create"),
    url(r'^favorite/(?P<quote_id>\d+)$', views.favorite_add, name = 'favorite'),
    url(r'^user/(?P<user_id>\d+)$', views.show_user, name = 'user'),
    url(r'^delete/(?P<quote_id>\d+)$', views.delete_quote, name = 'delete'),
]