from rest_framework import serializers
from .models import FactCheckResult

class FactCheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactCheckResult
        fields = [
            'id',
            'claim',
            'textual_rating',
            'verification_score',
            'evidence',
            'created_at'
        ]
