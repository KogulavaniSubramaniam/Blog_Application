from rest_framework import viewsets, permissions, status, generics, filters
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from datetime import datetime

class IsAdminOrAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name__in=['admin', 'author']).exists()
        return False

class PostSearchFilter(filters.SearchFilter):
    search_fields = ['title', 'content', 'author__username', 'created_at']

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrAuthor]
    filter_backends = [PostSearchFilter]


    def get_queryset(self):
        current_year = datetime.now().year
        return Post.objects.filter(created_at__year=current_year).order_by('-created_at')


    def perform_create(self, serializer):
        # Allow users to specify the created_at date if provided in request data
        created_at = self.request.data.get('created_at')
        if created_at:
            serializer.save(author=self.request.user, created_at=created_at)
        else:
            serializer.save(author=self.request.user)

class PostsByYearAPIView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        year = self.kwargs.get('year')
        queryset = Post.objects.filter(created_at__year=year)

        # Filter queryset based on query parameters
        title = self.request.query_params.get('title')
        content = self.request.query_params.get('content')
        author = self.request.query_params.get('author')

        if title:
            queryset = queryset.filter(title__icontains=title)
        if content:
            queryset = queryset.filter(content__icontains=content)
        if author:
            queryset = queryset.filter(author__username__icontains=author)

        return queryset.order_by('-created_at')
