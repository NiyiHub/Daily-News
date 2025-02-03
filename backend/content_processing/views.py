from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProcessedContent
from content_generation.models import GeneratedContent
from .utils import categorize_content, tag_content

class ProcessContentView(APIView):
    """
    API View for processing content that has been fact checked.
    It retrieves a GeneratedContent instance, categorizes and tags it,
    and then creates a ProcessedContent entry with AI gatekeeping applied.
    """

    def post(self, request, content_id):
        try:
            # Retrieve generated content by ID
            content = GeneratedContent.objects.get(id=content_id)
            
            # Check if the content is already processed
            if hasattr(content, 'processed_content'):
                return Response({"message": "Content has already been processed."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Categorize and tag the content using helper functions
            categories = categorize_content(content.body)
            tags = tag_content(content.body)
            
            # Create ProcessedContent entry; fact-check info and publish_status are computed in save()
            processed = ProcessedContent.objects.create(
                content=content,
                categories=categories,
                tags=tags
            )

            return Response({
                "message": "Content processed successfully.",
                "processed_content_id": processed.id,
                "categories": processed.categories,
                "tags": processed.tags,
                "fact_check_status": processed.fact_check_status,
                "composite_score": processed.composite_score,
                "publish_status": processed.publish_status,
            }, status=status.HTTP_201_CREATED)
        except GeneratedContent.DoesNotExist:
            return Response({"error": "Generated content not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
