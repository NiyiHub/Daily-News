from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProcessedContent, PublishedContent
from .serializers import ProcessedContentSerializer, PublishedContentSerializer
import logging

logger = logging.getLogger(__name__)

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
            from .utils import categorize_content, tag_content
            categories = categorize_content(content.body)
            tags = tag_content(content.body)
            processed = ProcessedContent.objects.create(
                content=content,
                categories=categories,
                tags=tags
            )
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
    This maps the news article ID to the corresponding PublishedContent and returns evidence.
    GET: Returns the evidence data or 404 if not found.
    """
    def get(self, request, news_id):
        print(f"\n{'='*60}")
        print(f"[EVIDENCE API] Called with news_id: {news_id}")
        print(f"{'='*60}")
        
        try:
            from content_generation.models import GeneratedContent
            
            # Step 1: Find GeneratedContent
            try:
                generated_content = GeneratedContent.objects.get(id=news_id)
                print(f"✅ [STEP 1] GeneratedContent found")
                print(f"   - ID: {generated_content.id}")
                print(f"   - Title: {generated_content.title}")
            except GeneratedContent.DoesNotExist:
                print(f"❌ [STEP 1] GeneratedContent NOT FOUND for ID {news_id}")
                return Response({
                    "error": "Article not found",
                    "message": "The requested article does not exist.",
                    "debug_info": f"No GeneratedContent with ID {news_id}"
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Step 2: Check ProcessedContent
            if not hasattr(generated_content, 'processed_content'):
                print(f"❌ [STEP 2] No ProcessedContent found")
                return Response({
                    "error": "No evidence available",
                    "message": "This article has not been fact-checked yet.",
                    "debug_info": "No processed_content relationship"
                }, status=status.HTTP_404_NOT_FOUND)
            
            processed_content = generated_content.processed_content
            print(f"✅ [STEP 2] ProcessedContent found")
            print(f"   - ID: {processed_content.id}")
            print(f"   - Fact check status: {processed_content.fact_check_status}")
            print(f"   - ProcessedContent evidence: {processed_content.evidence}")
            
            # Step 3: Check PublishedContent
            if not hasattr(processed_content, 'published_content'):
                print(f"❌ [STEP 3] No PublishedContent found")
                return Response({
                    "error": "No evidence available",
                    "message": "This article has not been published yet.",
                    "debug_info": "No published_content relationship"
                }, status=status.HTTP_404_NOT_FOUND)
            
            published_content = processed_content.published_content
            print(f"✅ [STEP 3] PublishedContent found")
            print(f"   - ID: {published_content.id}")
            print(f"   - Fact check status: {published_content.fact_check_status}")
            print(f"   - Evidence type: {type(published_content.evidence)}")
            print(f"   - Evidence value: {published_content.evidence}")
            print(f"   - Evidence is None: {published_content.evidence is None}")
            print(f"   - Evidence == {{}}: {published_content.evidence == {}}")
            print(f"   - not evidence: {not published_content.evidence}")
            
            # Step 4: Check evidence
            if published_content.evidence is None:
                print(f"❌ [STEP 4] Evidence is None")
                return Response({
                    "error": "No evidence available",
                    "message": "No verification evidence is available for this article.",
                    "has_evidence": False,
                    "debug_info": "evidence field is None"
                }, status=status.HTTP_404_NOT_FOUND)
            
            if published_content.evidence == {}:
                print(f"❌ [STEP 4] Evidence is empty dict")
                return Response({
                    "error": "No evidence available",
                    "message": "No verification evidence is available for this article.",
                    "has_evidence": False,
                    "debug_info": "evidence field is empty dict {}"
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Evidence exists!
            print(f"✅ [STEP 4] Evidence exists and is valid!")
            print(f"   - Evidence keys: {list(published_content.evidence.keys())}")
            
            response_data = {
                "evidence": published_content.evidence,
                "fact_check_status": published_content.fact_check_status,
                "has_evidence": True,
                "debug_info": {
                    "generated_content_id": generated_content.id,
                    "processed_content_id": processed_content.id,
                    "published_content_id": published_content.id
                }
            }
            
            print(f"✅ [SUCCESS] Returning 200 OK with evidence")
            print(f"{'='*60}\n")
            return Response(response_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"❌ [EXCEPTION] {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            print(f"{'='*60}\n")
            return Response({
                "error": "Server error",
                "message": str(e),
                "debug_info": f"{type(e).__name__}: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CategoryDetailView(APIView):
    """
    API view to retrieve categories for a specific ProcessedContent instance.
    """
    def get(self, request, processed_content_id):
        try:
            processed_content = ProcessedContent.objects.get(id=processed_content_id)
            categories = processed_content.categories
            return Response({"categories": categories}, status=status.HTTP_200_OK)
        except ProcessedContent.DoesNotExist:
            return Response({"error": "Processed content not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)