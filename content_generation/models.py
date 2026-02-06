from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

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
    """
    When an APIPrompt is saved with 'pending' status, generate content from it.
    """
    if created and instance.status == 'pending':
        # Import here to avoid circular imports
        from .utils import generate_content_from_prompt
        
        def _generate():
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
                instance.save(update_fields=['status'])
            except Exception as e:
                print(f"[ERROR] Content generation failed: {str(e)}")
                instance.status = 'error'
                instance.save(update_fields=['status'])
        
        # Execute after transaction commits to avoid database locks
        transaction.on_commit(_generate)


# Signal: When GeneratedContent is created, automatically trigger the full pipeline
@receiver(post_save, sender=GeneratedContent)
def trigger_content_pipeline(sender, instance, created, **kwargs):
    """
    When GeneratedContent is created, trigger:
    1. Fact checking
    2. Content processing (categorization, tagging, publishing)
    
    This single signal replaces the previous two separate signals to avoid race conditions.
    """
    if created:
        def _process_pipeline():
            try:
                print(f"[PIPELINE] Starting pipeline for: {instance.title} (ID: {instance.id})")
                
                # Step 1: Fact checking
                print(f"[PIPELINE] Step 1: Fact checking...")
                from fact_checking.utils import process_fact_check_for_content
                process_fact_check_for_content(instance)
                print(f"[PIPELINE] Fact checking complete")
                
                # Step 2: Content processing (categorization, tagging, publishing)
                print(f"[PIPELINE] Step 2: Content processing...")
                from content_processing.utils import process_generated_content
                process_generated_content(instance)
                print(f"[PIPELINE] Content processing complete")
                
                print(f"[PIPELINE] Pipeline complete for article ID {instance.id}")
                
            except Exception as e:
                print(f"[PIPELINE ERROR] Failed to process content: {type(e).__name__}: {str(e)}")
                import traceback
                traceback.print_exc()
        
        # Execute after transaction commits
        transaction.on_commit(_process_pipeline)