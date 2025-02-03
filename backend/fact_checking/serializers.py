# fact_checking/serializers.py

from rest_framework import serializers
from .models import FactCheckResult

class FactCheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactCheckResult
        fields = [
            'id',
            'claim',
            'disclosure_score',
            'source_score',
            'accuracy_score',
            'clarity_score',
            'composite_score',
            'details',
            'created_at'
        ]
