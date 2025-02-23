from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WrittenContent, WrittenImageContent, VideoContent
from .serializers import (
    WrittenContentSerializer, 
    WrittenImageContentSerializer, 
    VideoContentSerializer
)

# ---- WrittenContent Endpoints ----
class WrittenContentPostView(APIView):
    """
    API view to create WrittenContent via POST.
    Expects published_content, title, and content in the payload.
    """
    def post(self, request):
        serializer = WrittenContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Written content created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WrittenContentGetView(APIView):
    """
    API view to retrieve all WrittenContent records.
    """
    def get(self, request):
        contents = WrittenContent.objects.all()
        serializer = WrittenContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---- WrittenImageContent Endpoints ----
class WrittenImageContentPostView(APIView):
    """
    API view to create Written+Image content via POST.
    Expects published_content, title, content, and image_url in the payload.
    """
    def post(self, request):
        serializer = WrittenImageContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Written+Image content created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WrittenImageContentGetView(APIView):
    """
    API view to retrieve all Written+Image content records.
    """
    def get(self, request):
        contents = WrittenImageContent.objects.all()
        serializer = WrittenImageContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---- VideoContent Endpoints ----
class VideoContentPostView(APIView):
    """
    API view to create Video content via POST.
    Expects published_content, title, video_url, and summary in the payload.
    """
    def post(self, request):
        serializer = VideoContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Video content created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoContentGetView(APIView):
    """
    API view to retrieve all Video content records.
    """
    def get(self, request):
        contents = VideoContent.objects.all()
        serializer = VideoContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
