from .models import PostModel
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
  class Meta:
    model = PostModel
    fields =['id', 'title','description','created']
    
    
    