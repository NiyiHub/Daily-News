from django.contrib import admin
from .models import FactCheckResult

class FactCheckResultAdmin(admin.ModelAdmin):
    """
    Custom admin configuration for the FactCheckResult model.
    """
    list_display = ('claim', 'status', 'checked_at')  # Columns to display in the admin list view
    search_fields = ('claim',)  # Enable search by claim
    list_filter = ('status',)  # Add filter options for the status field
    ordering = ('-checked_at',)  # Order entries by the most recently checked

# Register the model with custom admin settings
admin.site.register(FactCheckResult, FactCheckResultAdmin)
