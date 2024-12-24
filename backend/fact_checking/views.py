from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import query_google_fact_check, query_news_api
from .models import FactCheckResult
from .serializers import FactCheckResultSerializer

class FactCheckView(APIView):
    """
    API View for fact-checking content.
    """

    def post(self, request):
        claim = request.data.get('claim')

        if not claim:
            return Response({"error": "Claim is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Query APIs
        google_result = query_google_fact_check(claim)
        news_result = query_news_api(claim)

        # Determine overall status
        final_status = google_result['status'] if google_result['status'] != "Unverified" else news_result['status']
        evidence = google_result['evidence'] or news_result['evidence']

        # Save result to database
        fact_check = FactCheckResult.objects.create(
            claim=claim,
            status=final_status,
            evidence=", ".join(evidence) if isinstance(evidence, list) else evidence
        )

        serializer = FactCheckResultSerializer(fact_check)
        return Response(serializer.data, status=status.HTTP_200_OK)
