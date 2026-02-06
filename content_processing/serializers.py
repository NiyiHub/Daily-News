from rest_framework import serializers
from .models import ProcessedContent, PublishedContent

class ProcessedContentSerializer(serializers.ModelSerializer):
    article_id = serializers.IntegerField(source='content.id', read_only=True)
    
    class Meta:
        model = ProcessedContent
        fields = [
            'id',
            'content',
            'article_id',  # The original GeneratedContent ID
            'categories',
            'tags',
            'fact_check_status',
            'composite_score',
            'evidence',
            'publish_status',
            'processed_at'
        ]

class PublishedContentSerializer(serializers.ModelSerializer):
    article_id = serializers.IntegerField(source='processed_content.content.id', read_only=True)
    
    class Meta:
        model = PublishedContent
        fields = [
            'id',
            'processed_content',
            'article_id',  # The original GeneratedContent ID
            'title',
            'body',
            'fact_check_status',
            'evidence',
            'tags',
            'image_url',
            'video_url',
            'published_at',
            'manually_overridden'
        ]