from rest_framework import serializers
from .models import (
    WrittenContent, WrittenContentLike, WrittenContentComment, WrittenContentShare,
    WrittenImageContent, WrittenImageContentLike, WrittenImageContentComment, WrittenImageContentShare,
    VideoContent, VideoContentLike, VideoContentComment, VideoContentShare
)

# Serializer for WrittenContent
class WrittenContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenContent
        fields = ['id', 'published_content', 'title', 'content', 'created_at']

# Serializer for WrittenContent interactive models
class WrittenContentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenContentLike
        fields = '__all__'

class WrittenContentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenContentComment
        fields = '__all__'

class WrittenContentShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenContentShare
        fields = '__all__'

# Serializer for WrittenImageContent
class WrittenImageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenImageContent
        fields = ['id', 'published_content', 'title', 'content', 'image_url', 'created_at']

# Serializers for WrittenImageContent interactive models
class WrittenImageContentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenImageContentLike
        fields = '__all__'

class WrittenImageContentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenImageContentComment
        fields = '__all__'

class WrittenImageContentShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = WrittenImageContentShare
        fields = '__all__'

# Serializer for VideoContent
class VideoContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContent
        fields = ['id', 'published_content', 'title', 'video_url', 'summary', 'created_at']

# Serializers for VideoContent interactive models
class VideoContentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContentLike
        fields = '__all__'

class VideoContentCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContentComment
        fields = '__all__'

class VideoContentShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoContentShare
        fields = '__all__'
