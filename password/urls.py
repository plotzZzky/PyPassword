from django.urls import path

from .import views


urlpatterns = [
    path('', views.open_db, name='open_db'),
    path('new/', views.generate_password, name='update_pwd'),
    path('list/', views.get_pwd_list, name='update_list'),
    path('props/name=<str:title>/', views.pwd_props, name='pwd_props'),
    path('del/name=<str:name>/', views.del_password, name='delete_pwd'),
    path('download/', views.download_db, name='download_db'),
]
