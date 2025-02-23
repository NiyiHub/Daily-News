from rest_framework import serializers
from .models import (
    WrittenContent, 
    WrittenContentLike, 
    WrittenContentComment, 
    WrittenContentShare,
    WrittenImageContent, 
    WrittenImageContentLike, 
    WrittenImageContentComment, 
    WrittenImageContentShare,
    VideoContent, 
    VideoContentLike, 
    VideoContentComment, 
    VideoContentShare
)

# --- Serializers for WrittenContent ---
class WrittenContentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    shares = serializers.SerializerMethodField()

    class Meta:
        model = WrittenContent
        fields = ['id', 'published_content', 'title', 'content', 'created_at', 'likes', 'comments', 'shares']

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return WrittenContentCommentSerializer(obj.comments.all(), many=True).data

    def get_shares(self, obj):
        return obj.shares.count()

class WrittenContentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenContentComment
        fields = ['id', 'text', 'created_at']


# --- Serializers for WrittenImageContent ---
class WrittenImageContentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    shares = serializers.SerializerMethodField()

    class Meta:
        model = WrittenImageContent
        fields = ['id', 'published_content', 'title', 'content', 'image_url', 'created_at', 'likes', 'comments', 'shares']

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return WrittenImageContentCommentSerializer(obj.comments.all(), many=True).data

    def get_shares(self, obj):
        return obj.shares.count()

class WrittenImageContentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenImageContentComment
        fields = ['id', 'text', 'created_at']


# --- Serializers for VideoContent ---
class VideoContentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    shares = serializers.SerializerMethodField()

    class Meta:
        model = VideoContent
        fields = ['id', 'published_content', 'title', 'video_url', 'summary', 'created_at', 'likes', 'comments', 'shares']

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        return VideoContentCommentSerializer(obj.comments.all(), many=True).data

    def get_shares(self, obj):
        return obj.shares.count()

class VideoContentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContentComment
        fields = ['id', 'text', 'created_at']
