from rest_framework import serializers
from .models import ProcessedContent, PublishedContent

class ProcessedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedContent
        fields = [
            'id',
            'content',
            'categories',
            'tags',
            'fact_check_status',
            'composite_score',
            'publish_status',
            'processed_at'
        ]

class PublishedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublishedContent
        fields = [
            'id',
            'processed_content',
            'title',
            'body',
            'fact_check_status',
            'tags',
            'image_url',
            'video_url',
            'published_at',
            'manually_overridden'
        ]
