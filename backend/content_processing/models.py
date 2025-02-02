from django.db import models
from content_generation.models import GeneratedContent
from fact_checking.models import FactCheckResult

class ProcessedContent(models.Model):
    """
    Stores metadata and categorization for verified content.
    Automatically retrieves fact-checking status and content from other apps.
    """
    content = models.OneToOneField(GeneratedContent, on_delete=models.CASCADE, related_name="processed_content")
    fact_check_status = models.CharField(max_length=20, editable=False)  # Retrieved from FactCheckResult
    reliability_score = models.FloatField(default=0.0)  # For added transparency
    categories = models.JSONField()  # E.g., ["AI", "Technology"]
    tags = models.JSONField()  # Dynamic tags for further granularity
    processed_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Override save() to automatically fetch fact-checking data
        and other metadata before saving.
        """
        # Fetch fact-checking status from FactCheckResult
        fact_check_result = FactCheckResult.objects.filter(claim=self.content.body).first()
        if fact_check_result:
            self.fact_check_status = fact_check_result.status
            self.reliability_score = 0.9 if self.fact_check_status == "Verified" else 0.5
        else:
            self.fact_check_status = "Unverified"
            self.reliability_score = 0.0

        super(ProcessedContent, self).save(*args, **kwargs)

    def __str__(self):
        return f"Processed Content for: {self.content.title} ({self.fact_check_status})"
