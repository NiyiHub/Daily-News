from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import GeneratedContent
from .serializers import GeneratedContentSerializer
from .utils import generate_content

class ContentGenerationView(APIView):
    """
    API View to handle content generation and storage.
    """

    def get(self, request):
        """
        Handle GET requests by returning a list of previously generated content.
        """
        generated_content = GeneratedContent.objects.all()  # Retrieve all generated content from the database
        serializer = GeneratedContentSerializer(generated_content, many=True)  # Serialize the data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Accepts a prompt, generates content via LLM, and stores it in the database.
        """
        prompt = request.data.get('prompt')
        temperature = request.data.get('temperature', 0.7)
        token_limit = request.data.get('token_limit', 256)

        # Validate input
        if not prompt:
            return Response({"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate content using the LLM
        result = generate_content(prompt, temperature, token_limit)

        # Save the content to the database
        generated_content = GeneratedContent.objects.create(
            title="Generated Title",  # You can refine this
            body=result['content'],
            prompt=prompt,
            temperature=temperature,
            token_limit=token_limit
        )

        # Serialize the response
        serializer = GeneratedContentSerializer(generated_content)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
