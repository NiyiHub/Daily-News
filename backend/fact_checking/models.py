from django.db import models

class FactCheckResult(models.Model):
    claim = models.TextField()  # The statement being fact-checked
    status = models.CharField(max_length=20, choices=[
        ('Verified', 'Verified'),
        ('False', 'False'),
        ('Partially True', 'Partially True'),
        ('Unverified', 'Unverified')
    ])  # Result of the fact check
    evidence = models.TextField(null=True, blank=True)  # Supporting evidence or references
    checked_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the check

    def __str__(self):
        return f"{self.claim[:50]}... ({self.status})"
