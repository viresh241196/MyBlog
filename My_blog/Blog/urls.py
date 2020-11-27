from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('new_post', views.new_post, name='new_post'),
    path('detail_post/<int:id>/', views.detail_post, name='detail_post'),
    path('user_posts/<int:author_id>/', views.user_post, name='user_posts'),
    path('update_post/<int:id>/', views.update_post, name='update_post'),
    path('post_comment', views.post_comment, name='post_comment'),
]
