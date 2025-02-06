# content_generation/models.py

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class APIPrompt(models.Model):
    """
    Model to store prompts for API content generation.
    """
    prompt_text = models.TextField()
    temperature = models.FloatField(default=0.7)
    token_limit = models.IntegerField(default=256)
    status = models.CharField(max_length=20, default='pending')  # pending, completed, error
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prompt: {self.prompt_text[:50]}..."

class GeneratedContent(models.Model):
    """
    Model to store the content generated from an APIPrompt.
    """
    prompt = models.ForeignKey(APIPrompt, on_delete=models.CASCADE, related_name='generated_contents')
    title = models.CharField(max_length=999)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Signal: When an APIPrompt is created, trigger content generation automatically.
@receiver(post_save, sender=APIPrompt)
def trigger_content_generation(sender, instance, created, **kwargs):
    if created and instance.status == 'pending':
        from .utils import generate_content_from_prompt
        try:
            result = generate_content_from_prompt(
                instance.prompt_text,
                temperature=instance.temperature,
                token_limit=instance.token_limit
            )
            GeneratedContent.objects.create(
                prompt=instance,
                title=result.get('title', 'Untitled'),
                body=result.get('body', '')
            )
            instance.status = 'completed'
            instance.save()
        except Exception as e:
            instance.status = 'error'
            instance.save()

# NEW Signal: When GeneratedContent is created, automatically trigger fact checking.
@receiver(post_save, sender=GeneratedContent)
def trigger_fact_check_for_generated_content(sender, instance, created, **kwargs):
    if created:
        try:
            from fact_checking.utils import process_fact_check_for_content
            process_fact_check_for_content(instance)
        except Exception as e:
            # Log the error or handle it appropriately; for now, we'll just print it.
            print("Error triggering fact check:", e)
