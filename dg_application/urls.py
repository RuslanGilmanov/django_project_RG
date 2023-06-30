from django.urls import path
from . import views as post_views
from .views import (PostListView,
                    PostDetailView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
                    )

urlpatterns = [
    path('', PostListView.as_view(), name='dgapp-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/create/', post_views.create_post, name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('tag/<str:tag>/', post_views.tags_view, name='tag-posts'),
    path('post_likes/<int:pk>', post_views.post_like, name='post-like'),
]

