from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    WrittenContentSerializer, WrittenImageContentSerializer, VideoContentSerializer
)

class CreateWrittenContentView(APIView):
    """
    API view for admin to manually create WrittenContent.
    Expects 'published_content', 'title', and 'content' in the request.
    """
    def post(self, request):
        serializer = WrittenContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Written content created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateWrittenImageContentView(APIView):
    """
    API view for admin to manually create Written+Image content.
    Expects 'published_content', 'title', 'content', and 'image_url' in the request.
    """
    def post(self, request):
        serializer = WrittenImageContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Written+Image content created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateVideoContentView(APIView):
    """
    API view for admin to manually create Video content.
    Expects 'published_content', 'title', 'video_url', and 'summary' in the request.
    """
    def post(self, request):
        serializer = VideoContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Video content created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
