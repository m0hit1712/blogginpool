from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs', views.main_blog_page, name='main_blog_page'),
    path('blog/<str:id_>', views.blog_view, name='blog_view'),
    path('dashboard/writer', views.blog_writers_dashboard, name='writers_dashboard'),
    path('create/blog', views.create_blog, name='create_blog'),
    path('edit/blog/<str:id_>', views.edit_blog, name='edit_blog'),
    path('blog/preview/<str:id_>', views.blog_preview, name='blog_preview'),
    path('create/save_draft', views.save_draft, name='save_draft_create'),
    path('dashboard/search', views.blog_search_bar, name='search_blog'),
    path('search', views.blog_search_bar, name='search_blog'),
    path('<str:name>', views.tag_blogs, name='tag_blogs'),
]
