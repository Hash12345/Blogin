from rest_framework import serializers
from .models import Post

class PostSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields='__all__'

        #fields=['id', 'title', 'body']

