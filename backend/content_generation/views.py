from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import APIPrompt, GeneratedContent
from .utils import generate_content_from_prompt

class ContentGenerationView(APIView):
    """
    API view to handle content generation via a provided prompt.
    Creates an APIPrompt record and then generates content using the OpenAI API.
    The resulting content is saved in GeneratedContent with a proper foreign key to APIPrompt.
    """

    def post(self, request):
        prompt_text = request.data.get('prompt_text')
        temperature = request.data.get('temperature', 0.7)
        token_limit = request.data.get('token_limit', 256)

        if not prompt_text:
            return Response({"error": "Prompt text is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create an APIPrompt record; this object will be used as the foreign key.
        prompt_obj = APIPrompt.objects.create(
            prompt_text=prompt_text,
            temperature=temperature,
            token_limit=token_limit,
            status='pending'
        )

        try:
            # Use the correct function from utils to generate content.
            result = generate_content_from_prompt(prompt_text, temperature=temperature, token_limit=token_limit)
            # Create GeneratedContent with the APIPrompt instance (prompt_obj) as the foreign key.
            GeneratedContent.objects.create(
                prompt=prompt_obj,
                title=result.get('title', 'Untitled'),
                body=result.get('body', '')
            )
            prompt_obj.status = 'completed'
            prompt_obj.save()
            return Response({"message": "Content generated successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            prompt_obj.status = 'error'
            prompt_obj.save()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
