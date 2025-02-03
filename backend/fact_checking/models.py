# fact_checking/models.py

from django.db import models

class FactCheckResult(models.Model):
    """
    Model to store the fact-checking results for a given generated content.
    Stores scores for multiple criteria and a composite score.
    """
    claim = models.TextField()  # Typically, the body of the generated content (or a key portion)
    disclosure_score = models.FloatField(default=0.0)       # Score for disclosure (0-1)
    source_score = models.FloatField(default=0.0)           # Score for source identification (0-1)
    accuracy_score = models.FloatField(default=0.0)         # Score for accuracy (0-1)
    clarity_score = models.FloatField(default=0.0)          # Score for clarity (0-1)
    composite_score = models.FloatField(default=0.0)        # Weighted average of the above scores
    details = models.JSONField(null=True, blank=True)       # Any additional fact-check details (e.g., evidence URLs)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FactCheck: {self.claim[:50]}... (Composite: {self.composite_score:.2f})"
