from django.contrib import admin
from .models import FactCheckResult

class FactCheckResultAdmin(admin.ModelAdmin):
    """
    Admin interface for FactCheckResult.
    """
    list_display = ('claim', 'textual_rating', 'verification_score', 'created_at')
    search_fields = ('claim',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)

admin.site.register(FactCheckResult, FactCheckResultAdmin)
