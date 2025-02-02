# content_generation/admin.py

from django.contrib import admin
from .models import GeneratedContent

@admin.register(GeneratedContent)
class GeneratedContentAdmin(admin.ModelAdmin):
    """
    Admin interface for GeneratedContent.
    Provides the ability to view and manually trigger generation if needed.
    """
    list_display = ('title', 'created_at')
    search_fields = ('title', 'body', 'prompt')

    # (Optional) You can add custom actions to re-trigger generation or other tasks.
    actions = ['regenerate_content']

    def regenerate_content(self, request, queryset):
        # This is a placeholder action. In a real-world scenario,
        # you might call the content generation function again.
        for content in queryset:
            # For demonstration, we simply print to the console.
            self.message_user(request, f"Re-generation triggered for: {content.title}")
    regenerate_content.short_description = "Regenerate selected content"
