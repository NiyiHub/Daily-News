from django.db import models
from content_generation.models import GeneratedContent
from fact_checking.models import FactCheckResult

PUBLISH_CHOICES = [
    ('published', 'Published'),
    ('withheld', 'Withheld')
]

class ProcessedContent(models.Model):
    """
    Model for processed content that has been categorized, tagged, and fact-checked.
    """
    content = models.OneToOneField(GeneratedContent, on_delete=models.CASCADE, related_name="processed_content")
    categories = models.JSONField(default=list, blank=True)  # e.g., ["AI", "Technology"]
    tags = models.JSONField(default=list, blank=True)  # Extracted tags/keywords
    fact_check_status = models.CharField(max_length=20, editable=False, blank=True)
    composite_score = models.FloatField(editable=False, default=0.0)
    evidence = models.JSONField(default=dict, blank=True, null=True)  # Store evidence from fact-checking
    publish_status = models.CharField(max_length=20, choices=PUBLISH_CHOICES, default='published')
    processed_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Override save() to retrieve fact-checking info and apply AI gatekeeping logic.
        Uses the fact-check result to determine publish_status:
          - If textual rating (TR) is "unverified", mark as 'published'
          - If TR is "verified", mark as 'withheld'
        """
        fact_check = FactCheckResult.objects.filter(claim=self.content.body).first()
        if fact_check:
            self.fact_check_status = fact_check.textual_rating
            self.composite_score = fact_check.verification_score
            self.evidence = fact_check.evidence  # Store the retrieved evidence
            # Determine publication status based on TR
            if self.fact_check_status.lower() == "unverified":
                self.publish_status = "published"
            elif self.fact_check_status.lower() == "verified":
                self.publish_status = "withheld"
            else:
                self.publish_status = "published"
        else:
            self.fact_check_status = "Unverified"
            self.composite_score = 0.0
            self.evidence = {}  # No evidence available
            self.publish_status = "published"
        super(ProcessedContent, self).save(*args, **kwargs)

    def __str__(self):
        return f"ProcessedContent for: {self.content.title} ({self.publish_status})"

class PublishedContent(models.Model):
    """
    Model for content that is ready to be published on the frontend.
    This includes text, fact-checking result, tags, multimedia fields, and evidence.
    """
    processed_content = models.OneToOneField(ProcessedContent, on_delete=models.CASCADE, related_name="published_content")
    title = models.CharField(max_length=999)
    body = models.TextField(max_length=5000)
    fact_check_status = models.CharField(max_length=20)
    evidence = models.JSONField(default=dict, blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    image_url = models.URLField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True, editable=False)
    manually_overridden = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Populate evidence from ProcessedContent if not manually overridden.
        """
        if not self.manually_overridden and self.processed_content:
            self.evidence = self.processed_content.evidence
        super(PublishedContent, self).save(*args, **kwargs)

    def __str__(self):
        return f"PublishedContent: {self.title}"

# NEW Signal: When ProcessedContent is created, automatically create a PublishedContent record if TR is "unverified".
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=ProcessedContent)
def trigger_publication(sender, instance, created, **kwargs):
    if created and instance.fact_check_status.lower() == "unverified":
        # Automatically publish if TR is "unverified"
        PublishedContent.objects.create(
            processed_content=instance,
            title=instance.content.title,
            body=instance.content.body,
            fact_check_status=instance.fact_check_status,
            tags=instance.tags
        )
