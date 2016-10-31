from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/register$', views.users_register, name='users_register'),
    url(r'^users/login$', views.login, name='login'),
    url(r'^users/manage$', views.users_manage, name='users_manage'),
    url(r'^users/logout$', views.users_logout, name='logout'),
    url(r'^users/(?P<id>\w+)$', views.show_user, name='show_user'),
    url(r'^users/delete/(?P<id>\w+)$', views.users_delete, name='users_delete'),
    url(r'^addfriend/(?P<id>\w+)$', views.add_friend, name='add_friend'),

]
