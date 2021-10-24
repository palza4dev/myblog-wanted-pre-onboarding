from django.urls import path

from posts.views import PostView, PostDetailView

urlpatterns = [
    path('', PostView.as_view()),
    path('/<int:post_id>', PostDetailView.as_view())
]