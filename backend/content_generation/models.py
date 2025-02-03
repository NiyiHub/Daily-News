from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class GeneratedContent(models.Model):
    """
    Model to store the generated news content.
    Includes a title and body.
    """
    title = models.CharField(max_length=255)  # Generated title
    body = models.TextField()                # Generated news content
    prompt = models.TextField()              # Prompt used for generation
    temperature = models.FloatField(default=0.7)  # Generation randomness parameter
    token_limit = models.IntegerField(default=256)  # Maximum tokens for the generated output
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Signal to trigger fact-checking automatically when new content is generated.
@receiver(post_save, sender=GeneratedContent)
def trigger_fact_check(sender, instance, created, **kwargs):
    if created:
        # Import here to avoid circular imports.
        from fact_checking.utils import process_fact_check_for_content
        process_fact_check_for_content(instance)
