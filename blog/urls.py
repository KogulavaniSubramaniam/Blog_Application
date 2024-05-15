from django.urls import path
from .views import PostViewSet, PostsByYearAPIView

urlpatterns = [
    path('api/posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name='post-list'),
    path('api/posts/<int:pk>/', PostViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='post-detail'),
    path('api/posts/year/<int:year>/', PostsByYearAPIView.as_view(), name='posts_by_year'),
]