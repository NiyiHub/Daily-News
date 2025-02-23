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

# --- Serializers for WrittenContent Interactive Features ---
class WrittenContentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenContentLike
        fields = ['id', 'created_at']

class WrittenContentCommentSerializer(serializers.ModelSerializer):
    # Include the foreign key field so that it can be saved from the view.
    written_content = serializers.PrimaryKeyRelatedField(queryset=WrittenContent.objects.all())

    class Meta:
        model = WrittenContentComment
        fields = ['id', 'written_content', 'text', 'created_at']

class WrittenContentShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenContentShare
        fields = ['id', 'written_content', 'platform', 'created_at']

# --- Serializer for WrittenContent ---
class WrittenContentSerializer(serializers.ModelSerializer):
    likes = WrittenContentLikeSerializer(many=True, read_only=True)
    comments = WrittenContentCommentSerializer(many=True, read_only=True)
    shares = WrittenContentShareSerializer(many=True, read_only=True)

    class Meta:
        model = WrittenContent
        fields = ['id', 'published_content', 'title', 'content', 'created_at', 'likes', 'comments', 'shares']


# --- Serializers for WrittenImageContent Interactive Features ---
class WrittenImageContentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenImageContentLike
        fields = ['id', 'created_at']

class WrittenImageContentCommentSerializer(serializers.ModelSerializer):
    written_image_content = serializers.PrimaryKeyRelatedField(queryset=WrittenImageContent.objects.all())

    class Meta:
        model = WrittenImageContentComment
        fields = ['id', 'written_image_content', 'text', 'created_at']

class WrittenImageContentShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenImageContentShare
        fields = ['id', 'written_image_content', 'platform', 'created_at']

# --- Serializer for WrittenImageContent ---
class WrittenImageContentSerializer(serializers.ModelSerializer):
    likes = WrittenImageContentLikeSerializer(many=True, read_only=True)
    comments = WrittenImageContentCommentSerializer(many=True, read_only=True)
    shares = WrittenImageContentShareSerializer(many=True, read_only=True)

    class Meta:
        model = WrittenImageContent
        fields = ['id', 'published_content', 'title', 'content', 'image_url', 'created_at', 'likes', 'comments', 'shares']


# --- Serializers for VideoContent Interactive Features ---
class VideoContentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContentLike
        fields = ['id', 'created_at']

class VideoContentCommentSerializer(serializers.ModelSerializer):
    video_content = serializers.PrimaryKeyRelatedField(queryset=VideoContent.objects.all())

    class Meta:
        model = VideoContentComment
        fields = ['id', 'video_content', 'text', 'created_at']

class VideoContentShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContentShare
        fields = ['id', 'video_content', 'platform', 'created_at']

# --- Serializer for VideoContent ---
class VideoContentSerializer(serializers.ModelSerializer):
    likes = VideoContentLikeSerializer(many=True, read_only=True)
    comments = VideoContentCommentSerializer(many=True, read_only=True)
    shares = VideoContentShareSerializer(many=True, read_only=True)

    class Meta:
        model = VideoContent
        fields = ['id', 'published_content', 'title', 'video_url', 'summary', 'created_at', 'likes', 'comments', 'shares']
