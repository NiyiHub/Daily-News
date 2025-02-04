from django.db import models
from content_generation.models import GeneratedContent
from fact_checking.models import FactCheckResult

PUBLISH_CHOICES = [
    ('published', 'Published'),
    ('withheld', 'Withheld')
]

class ProcessedContent(models.Model):
    """
    Model for processed content.
    This includes categorization, tagging, fact-check metadata,
    and an AI gatekeeping field for publish status.
    """
    content = models.OneToOneField(GeneratedContent, on_delete=models.CASCADE, related_name="processed_content")
    categories = models.JSONField(default=list, blank=True)  # Provides an empty list by default
    tags = models.JSONField(default=list, blank=True)
    fact_check_status = models.CharField(max_length=20, editable=False)  # Taken from FactCheckResult
    composite_score = models.FloatField(editable=False, default=0.0)     # Fact-check composite score
    publish_status = models.CharField(max_length=20, choices=PUBLISH_CHOICES, default='published')
    processed_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Override save to automatically retrieve fact-checking data.
        Also, determine the publish_status via AI gatekeeping logic:
         - If composite_score is HIGH (>= threshold), mark as 'withheld'
         - Otherwise, mark as 'published'
        """
        # Attempt to retrieve FactCheckResult based on content.body
        fact_check = FactCheckResult.objects.filter(claim=self.content.body).first()
        if fact_check:
            self.fact_check_status = "Verified" if fact_check.composite_score >= 0.7 else "Unverified"
            self.composite_score = fact_check.composite_score

            # AI gatekeeping logic: Withhold if composite score is high (i.e. very factual)
            # Let's assume threshold is 0.7: scores >= 0.7 (very factual) are withheld
            if self.composite_score >= 0.7:
                self.publish_status = "withheld"
            else:
                self.publish_status = "published"
        else:
            self.fact_check_status = "Unverified"
            self.composite_score = 0.0
            self.publish_status = "published"
        
        super(ProcessedContent, self).save(*args, **kwargs)

    def __str__(self):
        return f"ProcessedContent for: {self.content.title} ({self.publish_status})"
