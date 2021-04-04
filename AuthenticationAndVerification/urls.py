from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('del', views.delete_session, name="del"),
    path('activate/<uname_b64>/<token>/', views.activate, name='activate'),
    path('reset_password/<uname_b64>/<token>',views.reset_password, name='reset_password'),
    path('profile', views.blog_writers_profile, name="profile"),
    path('profile/<int:id_>',views.blog_writers_profile,name="see_profile"),
    path('edit_profile/<int:id_>', views.edit_profile, name="edit_profile"),
]
