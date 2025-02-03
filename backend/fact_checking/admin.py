from django.contrib import admin
from .models import FactCheckResult

class FactCheckResultAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for FactCheckResult.
    Displays claim, composite_score, and created_at.
    """
    list_display = ('claim', 'composite_score', 'created_at')
    search_fields = ('claim',)
    list_filter = ('created_at',)  # You can change this to any field you prefer.
    ordering = ('-created_at',)

admin.site.register(FactCheckResult, FactCheckResultAdmin)
