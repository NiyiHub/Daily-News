from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import process_fact_check_manual
from .models import FactCheckResult
from .serializers import FactCheckResultSerializer

class FactCheckView(APIView):
    """
    API view to manually process fact checking for a given claim.
    """
    def post(self, request):
        claim = request.data.get('claim')
        if not claim:
            return Response({"error": "Claim is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result = process_fact_check_manual(claim)
            serializer = FactCheckResultSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
