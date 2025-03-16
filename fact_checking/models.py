from django.db import models

class FactCheckResult(models.Model):
    """
    Model to store fact-checking results for a given claim using the Google Fact Check API.
    """
    claim = models.TextField()  # The claim or content being fact checked
    verification_score = models.FloatField(default=0.0)  # Composite score computed from factors
    textual_rating = models.CharField(max_length=50, blank=True)  # E.g., "TRUE", "FALSE", etc.
    evidence = models.JSONField(default=dict, null=True, blank=True)  # Stores evidence details (e.g., URLs, excerpts)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the fact check was performed

    def __str__(self):
        return f"FactCheckResult ({self.textual_rating}) for: {self.claim[:50]}..."
