from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^register$', views.register, name='register'),
    url(r'^users/register$', views.users_register, name='users_register'),
    url(r'^users/login$', views.login, name='login'),
    url(r'^users/manage$', views.users_manage, name='users_manage'),
    url(r'^users/logout$', views.users_logout, name='logout'),
    url(r'^users/update/(?P<id>\w+)$', views.users_update, name='update'),
    url(r'^users/pass/(?P<id>\w+)$', views.update_password, name='pass'),
    url(r'^users/edit/(?P<id>\w+)$', views.users_edit, name='edit'),
    url(r'^users/delete/(?P<id>\w+)$', views.users_delete, name='users_delete'),
    url(r'^users/wall/(?P<id>\w+)$', views.users_wall, name='wall'),
    url(r'^messages/post/(?P<id>\w+)$', views.post_messages, name='post_message'),
    url(r'^Comments/post/(?P<id>\w+)/(?P<user>\w+)$', views.post_comment, name='post_comment'),
    url(r'^messages/delete/(?P<id>\w+)$', views.delete_messages, name='delete_message'),
    url(r'^comments/delete/(?P<id>\w+)/(?P<user>\w+)$', views.delete_comment, name='delete_comment'),

]
