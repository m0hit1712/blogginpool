from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('del', views.delete_session, name="del"),
    path('activate/<uname_b64>/<token>/', views.activate, name='activate'),
    path('reset_password/<uname_b64>/<token>',views.reset_password, name='reset_password'),
    path('profile/<str:uname>',views.blog_writers_profile,name="see_profile"),
    path('edit_profile', views.edit_profile, name="edit_profile"),
    path('ajax/verify_email', views.ajax_verify_email, name="ajax_verify_email"),
]
