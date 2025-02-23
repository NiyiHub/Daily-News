from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    WrittenContent, 
    WrittenContentLike, 
    WrittenContentComment, 
    WrittenContentShare,

    WrittenImageContent, 
    WrittenImageContentLike, 
    WrittenImageContentComment, 
    WrittenImageContentShare,

    VideoContent, 
    VideoContentLike, 
    VideoContentComment, 
    VideoContentShare
)
from .serializers import (
    WrittenContentSerializer, 
    WrittenContentCommentSerializer, 
    WrittenContentLikeSerializer, 
    WrittenContentShareSerializer,

    WrittenImageContentSerializer, 
    WrittenImageContentCommentSerializer, 
    WrittenImageContentLikeSerializer, 
    WrittenImageContentShareSerializer,

    VideoContentSerializer, 
    VideoContentCommentSerializer, 
    VideoContentLikeSerializer, 
    VideoContentShareSerializer
)

# ---- WrittenContent Endpoints ----
class WrittenContentPostView(APIView):
    def post(self, request):
        serializer = WrittenContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Written content created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WrittenContentGetView(APIView):
    def get(self, request):
        contents = WrittenContent.objects.all()
        serializer = WrittenContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WrittenContentCommentView(APIView):
    def get(self, request, written_content_id):
        try:
            comments = WrittenContentComment.objects.filter(written_content_id=written_content_id)
            serializer = WrittenContentCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, written_content_id):
        data = request.data.copy()
        data['written_content'] = written_content_id
        serializer = WrittenContentCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Comment added successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WrittenContentLikeView(APIView):
    def post(self, request, written_content_id):
        try:
            WrittenContentLike.objects.create(written_content_id=written_content_id)
            return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WrittenContentShareView(APIView):
    def post(self, request, written_content_id):
        data = request.data.copy()
        data['written_content'] = written_content_id
        try:
            WrittenContentShare.objects.create(
                written_content_id=written_content_id,
                platform=data.get('platform', 'Unknown')
            )
            return Response({"message": "Share added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---- WrittenImageContent Endpoints ----
class WrittenImageContentPostView(APIView):
    def post(self, request):
        serializer = WrittenImageContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Written+Image content created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WrittenImageContentGetView(APIView):
    def get(self, request):
        contents = WrittenImageContent.objects.all()
        serializer = WrittenImageContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class WrittenImageContentCommentView(APIView):
    def get(self, request, written_image_content_id):
        try:
            comments = WrittenImageContentComment.objects.filter(written_image_content_id=written_image_content_id)
            serializer = WrittenImageContentCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, written_image_content_id):
        data = request.data.copy()
        data['written_image_content'] = written_image_content_id
        serializer = WrittenImageContentCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Comment added successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WrittenImageContentLikeView(APIView):
    def post(self, request, written_image_content_id):
        try:
            WrittenImageContentLike.objects.create(written_image_content_id=written_image_content_id)
            return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WrittenImageContentShareView(APIView):
    def post(self, request, written_image_content_id):
        data = request.data.copy()
        data['written_image_content'] = written_image_content_id
        try:
            WrittenImageContentShare.objects.create(
                written_image_content_id=written_image_content_id,
                platform=data.get('platform', 'Unknown')
            )
            return Response({"message": "Share added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ---- VideoContent Endpoints ----
class VideoContentPostView(APIView):
    def post(self, request):
        serializer = VideoContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Video content created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoContentGetView(APIView):
    def get(self, request):
        contents = VideoContent.objects.all()
        serializer = VideoContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class VideoContentCommentView(APIView):
    def get(self, request, video_content_id):
        try:
            comments = VideoContentComment.objects.filter(video_content_id=video_content_id)
            serializer = VideoContentCommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, video_content_id):
        data = request.data.copy()
        data['video_content'] = video_content_id
        serializer = VideoContentCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Comment added successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VideoContentLikeView(APIView):
    def post(self, request, video_content_id):
        try:
            VideoContentLike.objects.create(video_content_id=video_content_id)
            return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VideoContentShareView(APIView):
    def post(self, request, video_content_id):
        data = request.data.copy()
        data['video_content'] = video_content_id
        try:
            VideoContentShare.objects.create(
                video_content_id=video_content_id,
                platform=data.get('platform', 'Unknown')
            )
            return Response({"message": "Share added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
