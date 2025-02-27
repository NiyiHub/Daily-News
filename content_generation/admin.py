from django.contrib import admin
from .models import APIPrompt, GeneratedContent

@admin.register(APIPrompt)
class APIPromptAdmin(admin.ModelAdmin):
    """
    Admin interface for APIPrompt. Allows manual prompting.
    """
    list_display = ('prompt_text', 'status', 'created_at')
    search_fields = ('prompt_text',)
    actions = ['trigger_generation']

    def trigger_generation(self, request, queryset):
        for prompt in queryset.filter(status='pending'):
            from .utils import generate_content_from_prompt
            try:
                result = generate_content_from_prompt(
                    prompt.prompt_text,
                    temperature=prompt.temperature,
                    token_limit=prompt.token_limit
                )
                prompt.generated_contents.create(
                    title=result.get('title', 'Untitled'),
                    body=result.get('body', '')
                )
                prompt.status = 'completed'
                prompt.save()
                self.message_user(request, f"Content generated for prompt: {prompt.prompt_text[:50]}...")
            except Exception as e:
                prompt.status = 'error'
                prompt.save()
                self.message_user(request, f"Error for prompt: {prompt.prompt_text[:50]}: {str(e)}")
    trigger_generation.short_description = "Trigger content generation for selected prompts"

@admin.register(GeneratedContent)
class GeneratedContentAdmin(admin.ModelAdmin):
    """
    Admin interface for GeneratedContent.
    """
    list_display = ('title', 'prompt', 'created_at')
    search_fields = ('title', 'body')
