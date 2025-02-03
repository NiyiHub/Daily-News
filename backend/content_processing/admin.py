from django.contrib import admin
from .models import ProcessedContent

@admin.register(ProcessedContent)
class ProcessedContentAdmin(admin.ModelAdmin):
    """
    Admin interface for ProcessedContent.
    Allows admin to review processed content and manually override publish_status.
    """
    list_display = ('content', 'fact_check_status', 'composite_score', 'publish_status', 'processed_at')
    list_filter = ('publish_status', 'fact_check_status')
    search_fields = ('content__title',)
    readonly_fields = ('composite_score', 'fact_check_status', 'categories', 'tags', 'processed_at')
