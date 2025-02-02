from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProcessedContent
from content_generation.models import GeneratedContent
from .utils import categorize_content, tag_content

class ProcessContentView(APIView):
    """
    API View to process verified content and generate metadata like categories and tags.
    """

    def post(self, request, content_id):
        try:
            # Fetch the GeneratedContent entry
            content = GeneratedContent.objects.get(id=content_id)

            # Check if the content has already been processed
            if ProcessedContent.objects.filter(content=content).exists():
                return Response({"message": "Content has already been processed."}, status=status.HTTP_400_BAD_REQUEST)

            # Categorize and tag the content
            categories = categorize_content(content.body)
            tags = tag_content(content.body)

            # Create a new ProcessedContent entry (fact-checking status fetched automatically via save())
            processed_content = ProcessedContent.objects.create(
                content=content,
                categories=categories,
                tags=tags
            )

            return Response(
                {
                    "message": "Content processed successfully.",
                    "content_id": processed_content.id,
                    "categories": categories,
                    "tags": tags,
                    "fact_check_status": processed_content.fact_check_status,
                    "reliability_score": processed_content.reliability_score,
                },
                status=status.HTTP_201_CREATED
            )
        except GeneratedContent.DoesNotExist:
            return Response({"error": "Content not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
