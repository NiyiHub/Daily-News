from rest_framework import serializers
from .models import APIPrompt, GeneratedContent

class APIPromptSerializer(serializers.ModelSerializer):
    """
    Serializer for the APIPrompt model.
    """
    class Meta:
        model = APIPrompt
        fields = ['id', 'prompt_text', 'temperature', 'token_limit', 'status', 'created_at']

class GeneratedContentSerializer(serializers.ModelSerializer):
    """
    Serializer for the GeneratedContent model, with a nested representation for the prompt.
    """
    prompt = APIPromptSerializer(read_only=True)
    
    class Meta:
        model = GeneratedContent
        fields = ['id', 'title', 'body', 'prompt', 'temperature', 'token_limit', 'created_at']
