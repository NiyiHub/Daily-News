from django.db import models

class FactCheckResult(models.Model):
    """
    Model to store fact-checking results based on multiple criteria.
    """
    claim = models.TextField()  # Claim being fact-checked (typically the content body)
    disclosure_score = models.FloatField(default=0.0)
    source_score = models.FloatField(default=0.0)
    accuracy_score = models.FloatField(default=0.0)
    clarity_score = models.FloatField(default=0.0)
    composite_score = models.FloatField(default=0.0)  # Weighted average of criteria
    details = models.JSONField(null=True, blank=True)  # Evidence and additional info
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FactCheck: {self.claim[:50]}... (Composite: {self.composite_score:.2f})"