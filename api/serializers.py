from rest_framework import serializers
from .models import Category, Reply, Topic, Comment, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model= Topic
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Comment
        fields = '__all__'

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model= Reply
        fields = '__all__'

