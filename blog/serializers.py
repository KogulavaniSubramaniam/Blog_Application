from rest_framework import serializers
from .models import Post
from datetime import datetime

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    created_at = serializers.DateTimeField(default=datetime.now) 
    

    class Meta:
        model = Post
        fields = '__all__'
