from rest_framework import serializers
from .models import FactCheckResult

class FactCheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactCheckResult
        fields = ['id', 'claim', 'status', 'evidence', 'checked_at']
