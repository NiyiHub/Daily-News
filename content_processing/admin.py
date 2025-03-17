from django.contrib import admin
from .models import ProcessedContent, PublishedContent

@admin.register(ProcessedContent)
class ProcessedContentAdmin(admin.ModelAdmin):
    list_display = ('content', 'fact_check_status', 'composite_score', 'publish_status', 'processed_at')
    list_filter = ('publish_status', 'fact_check_status')
    readonly_fields = ('fact_check_status', 'composite_score', 'evidence')
    search_fields = ('content__title',)

@admin.register(PublishedContent)
class PublishedContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'fact_check_status', 'published_at', 'manually_overridden')
    list_filter = ('manually_overridden', 'fact_check_status')
    fields = ('processed_content', 'title', 'body', 'fact_check_status', 'evidence', 'tags', 'image_url', 'video_url', 'published_at', 'manually_overridden')
    search_fields = ('title', 'fact_check_status')
    readonly_fields = ('published_at',)
