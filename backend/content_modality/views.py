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
    WrittenImageContentSerializer, 
    VideoContentSerializer,

    WrittenContentCommentSerializer, 
    WrittenImageContentCommentSerializer, 
    VideoContentCommentSerializer
)

# --- WrittenContent Endpoints ---
class WrittenContentPostView(APIView):
    """
    API view to create WrittenContent.
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

class WrittenContentCommentView(APIView):
    """
    API view to handle comments for a specific WrittenContent record.
    GET: Retrieve all comments.
    POST: Create a new comment.
    """
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
    """
    API view to add a like to a specific WrittenContent record.
    """
    def post(self, request, written_content_id):
        try:
            like = WrittenContentLike.objects.create(written_content_id=written_content_id)
            return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WrittenContentShareView(APIView):
    """
    API view to add a share to a specific WrittenContent record.
    Expects 'platform' in the request payload.
    """
    def post(self, request, written_content_id):
        data = request.data.copy()
        data['written_content'] = written_content_id
        try:
            share = WrittenContentShare.objects.create(
                written_content_id=written_content_id,
                platform=data.get('platform', 'Unknown')
            )
            return Response({"message": "Share added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# --- WrittenImageContent Endpoints ---
class WrittenImageContentPostView(APIView):
    """
    API view to create Written+Image content.
    Expects published_content, title, content, and image_url.
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

class WrittenImageContentCommentView(APIView):
    """
    API view to handle comments for a specific WrittenImageContent record.
    GET: Retrieve comments.
    POST: Add a new comment.
    """
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
    """
    API view to add a like to a specific WrittenImageContent record.
    """
    def post(self, request, written_image_content_id):
        try:
            like = WrittenImageContentLike.objects.create(written_image_content_id=written_image_content_id)
            return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WrittenImageContentShareView(APIView):
    """
    API view to add a share to a specific WrittenImageContent record.
    Expects 'platform' in the payload.
    """
    def post(self, request, written_image_content_id):
        data = request.data.copy()
        data['written_image_content'] = written_image_content_id
        try:
            share = WrittenImageContentShare.objects.create(
                written_image_content_id=written_image_content_id,
                platform=data.get('platform', 'Unknown')
            )
            return Response({"message": "Share added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# --- VideoContent Endpoints ---
class VideoContentPostView(APIView):
    """
    API view to create Video content.
    Expects published_content, title, video_url, and summary.
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

class VideoContentCommentView(APIView):
    """
    API view to handle comments for a specific VideoContent record.
    GET: Retrieve comments.
    POST: Add a new comment.
    """
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
    """
    API view to add a like to a specific VideoContent record.
    """
    def post(self, request, video_content_id):
        try:
            like = VideoContentLike.objects.create(video_content_id=video_content_id)
            return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VideoContentShareView(APIView):
    """
    API view to add a share to a specific VideoContent record.
    Expects 'platform' in the payload.
    """
    def post(self, request, video_content_id):
        data = request.data.copy()
        data['video_content'] = video_content_id
        try:
            share = VideoContentShare.objects.create(
                video_content_id=video_content_id,
                platform=data.get('platform', 'Unknown')
            )
            return Response({"message": "Share added successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
