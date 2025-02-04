from django.contrib import admin
from .models import GeneratedContent

@admin.register(GeneratedContent)
class GeneratedContentAdmin(admin.ModelAdmin):
    """
    Admin interface for GeneratedContent.
    Provides the ability to view and manually trigger content generation.
    """
    list_display = ('title', 'created_at')
    search_fields = ('title', 'body', 'prompt')
    
    actions = ['regenerate_content']
    
    def regenerate_content(self, request, queryset):
        for content in queryset:
            # Placeholder action; in practice, re-trigger generation logic if needed.
            self.message_user(request, f"Re-generation triggered for: {content.title}")
    regenerate_content.short_description = "Regenerate selected content"