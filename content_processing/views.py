from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProcessedContent, PublishedContent
from .serializers import ProcessedContentSerializer, PublishedContentSerializer

class ProcessContentView(APIView):
    """
    API view to manually process a GeneratedContent instance.
    It categorizes, tags, and creates a ProcessedContent record.
    Based on fact-check textual rating (TR), content may be automatically published.
    """
    def post(self, request, content_id):
        try:
            from content_generation.models import GeneratedContent
            content = GeneratedContent.objects.get(id=content_id)
            if hasattr(content, 'processed_content'):
                return Response({"message": "Content has already been processed."}, status=status.HTTP_400_BAD_REQUEST)
            # Assume categorize_content and tag_content are utility functions used here
            from .utils import categorize_content, tag_content
            categories = categorize_content(content.body)
            tags = tag_content(content.body)
            processed = ProcessedContent.objects.create(
                content=content,
                categories=categories,
                tags=tags
            )
            # Automatically publish if TR is unverified (handled in save())
            if processed.publish_status == "published":
                from .models import PublishedContent
                PublishedContent.objects.create(
                    processed_content=processed,
                    title=content.title,
                    body=content.body, 
                    fact_check_status=processed.fact_check_status,
                    tags=processed.tags
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

class PublishedContentEvidenceView(APIView):
    """
    API view to retrieve and update the evidence field of a PublishedContent record.
    GET: Returns the evidence data.
    PUT/PATCH: Updates the evidence field.
    """
    def get(self, request, published_content_id):
        try:
            published = PublishedContent.objects.get(id=published_content_id)
            data = {"evidence": published.evidence}
            return Response(data, status=status.HTTP_200_OK)
        except PublishedContent.DoesNotExist:
            return Response({"error": "Published content not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, published_content_id):
        try:
            published = PublishedContent.objects.get(id=published_content_id)
            new_evidence = request.data.get("evidence")
            if new_evidence is None:
                return Response({"error": "Evidence data is required."}, status=status.HTTP_400_BAD_REQUEST)
            published.evidence = new_evidence
            published.save()
            return Response({"message": "Evidence updated successfully.", "evidence": published.evidence}, status=status.HTTP_200_OK)
        except PublishedContent.DoesNotExist:
            return Response({"error": "Published content not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NewsArticleEvidenceView(APIView):
    """
    API view to retrieve evidence for a news article by its ID.
    This maps the news article ID (GeneratedContent ID) to the corresponding 
    PublishedContent and returns evidence.
    
    GET: Returns the evidence data or appropriate message if not available.
    """
    def get(self, request, news_id):
        try:
            # Import here to avoid circular imports
            from content_generation.models import GeneratedContent
            
            # Find the GeneratedContent by news_id
            try:
                generated_content = GeneratedContent.objects.get(id=news_id)
            except GeneratedContent.DoesNotExist:
                return Response({
                    "error": "Article not found",
                    "message": "The requested article does not exist.",
                    "has_evidence": False
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Check if it has been processed
            if not hasattr(generated_content, 'processed_content'):
                return Response({
                    "error": "Not processed",
                    "message": "This article has not been fact-checked yet.",
                    "has_evidence": False,
                    "article_id": news_id
                }, status=status.HTTP_200_OK)  # Changed to 200 since article exists
            
            processed_content = generated_content.processed_content
            
            # Check if it has been published
            if not hasattr(processed_content, 'published_content'):
                return Response({
                    "error": "Not published",
                    "message": "This article has not been published yet.",
                    "has_evidence": False,
                    "article_id": news_id,
                    "fact_check_status": processed_content.fact_check_status
                }, status=status.HTTP_200_OK)  # Changed to 200 since article exists
            
            published_content = processed_content.published_content
            
            # Check if evidence exists and is not empty
            # Note: Admin might choose not to include evidence
            if not published_content.evidence or published_content.evidence == {}:
                return Response({
                    "message": "No evidence available for this article.",
                    "has_evidence": False,
                    "article_id": news_id,
                    "published_content_id": published_content.id,
                    "fact_check_status": published_content.fact_check_status,
                    "title": published_content.title
                }, status=status.HTTP_200_OK)
            
            # Return evidence data with all relevant IDs for debugging
            return Response({
                "evidence": published_content.evidence,
                "fact_check_status": published_content.fact_check_status,
                "has_evidence": True,
                "article_id": news_id,
                "published_content_id": published_content.id,
                "processed_content_id": processed_content.id,
                "title": published_content.title
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": "Server error",
                "message": str(e),
                "has_evidence": False
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryDetailView(APIView):
    """
    API view to retrieve categories for a specific ProcessedContent instance.
    """
    def get(self, request, processed_content_id):
        try:
            processed_content = ProcessedContent.objects.get(id=processed_content_id)
            categories = processed_content.categories  # Assuming this is stored as a list or a string

            return Response({"categories": categories}, status=status.HTTP_200_OK)
        except ProcessedContent.DoesNotExist:
            return Response({"error": "Processed content not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)