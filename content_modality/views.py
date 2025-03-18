from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import views, status
from .models import (
    UserSession,
    UserBookmark,

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
    UserSessionSerializer,

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

# ---- User Session Views ----
class UserLoginView(views.APIView):
    """Handles user session creation."""
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        session = UserSession.create_session(user_id)
        return Response({
            "user_id": session.user_id,
            "session_token": session.session_token,
            "created_at": session.created_at,
            "last_active": session.last_active
        }, status=status.HTTP_200_OK)
    


class UserSessionView(views.APIView):
    """Handles session validation."""
    def get(self, request):
        session_token = request.headers.get("Authorization")
        if not session_token:
            return Response({"error": "Session token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            session = UserSession.objects.get(session_token=session_token)
            session.update_last_active()
            return Response({
                "user_id": session.user_id,
                "session_token": session.session_token,
                "last_active": session.last_active
            }, status=status.HTTP_200_OK)
        except UserSession.DoesNotExist:
            return Response({"error": "Invalid session token."}, status=status.HTTP_401_UNAUTHORIZED)
        

# ---- Bookmark View ----
class UserBookmarkView(APIView):
    def post(self, request, written_content_id):
        user_id = request.data.get("user_id")
        content_id = request.data.get("content_id")
        content_type = request.data.get("content_type")

        if not user_id or not content_id or not content_type:
            return Response({"error": "User ID, content ID, and content type are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserSession.objects.get(user_id=user_id)
            UserBookmark.objects.create(user=user, content_id=written_content_id, content_type=content_type)
            return Response({"message": "Bookmark added successfully."}, status=status.HTTP_201_CREATED)
        except UserSession.DoesNotExist:
            return Response({"error": "User session not found."}, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request):
        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserSession.objects.get(user_id=user_id)
            bookmarks = UserBookmark.objects.filter(user=user)
            bookmark_data = [{"content_id": b.content_id, "content_type": b.content_type, "created_at": b.created_at} for b in bookmarks]
            return Response({"bookmarks": bookmark_data}, status=status.HTTP_200_OK)
        except UserSession.DoesNotExist:
            return Response({"error": "User session not found."}, status=status.HTTP_400_BAD_REQUEST)

        
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
        user_id = request.data.get("user_id")
        text = request.data.get("text")

        if not user_id or not text:
            return Response({"error": "User ID and comment text are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserSession.objects.get(user_id=user_id)
            WrittenContentComment.objects.create(user=user, written_content_id=written_content_id, text=text)
            return Response({"message": "Comment added successfully."}, status=status.HTTP_201_CREATED)
        except UserSession.DoesNotExist:
            return Response({"error": "User session not found."}, status=status.HTTP_400_BAD_REQUEST)


class WrittenContentLikeView(APIView):
    def post(self, request, written_content_id):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserSession.objects.get(user_id=user_id)
            WrittenContentLike.objects.create(user=user, written_content_id=written_content_id)
            return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
        except UserSession.DoesNotExist:
            return Response({"error": "User session not found."}, status=status.HTTP_400_BAD_REQUEST)


class WrittenContentShareView(APIView):
    def post(self, request, written_content_id):
        user_id = request.data.get("user_id")
        platform = request.data.get("platform", "Unknown")

        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserSession.objects.get(user_id=user_id)
            WrittenContentShare.objects.create(user=user, written_content_id=written_content_id, platform=platform)
            return Response({"message": "Share added successfully."}, status=status.HTTP_201_CREATED)
        except UserSession.DoesNotExist:
            return Response({"error": "User session not found."}, status=status.HTTP_400_BAD_REQUEST)


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
        user_id = request.data.get("user_id")
        text = request.data.get("text")

        if not user_id or not text:
            return Response({"error": "User ID and comment text are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserSession.objects.get(user_id=user_id)
            WrittenImageContentComment.objects.create(user=user, written_image_content_id=written_image_content_id, text=text)
            return Response({"message": "Comment added successfully."}, status=status.HTTP_201_CREATED)
        except UserSession.DoesNotExist:
            return Response({"error": "User session not found."}, status=status.HTTP_400_BAD_REQUEST)

class WrittenImageContentLikeView(APIView):
    def post(self, request, written_image_content_id):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserSession.objects.get(user_id=user_id)
            WrittenImageContentLike.objects.create(user=user, written_image_content_id=written_image_content_id)
            return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
        except UserSession.DoesNotExist:
            return Response({"error": "User session not found."}, status=status.HTTP_400_BAD_REQUEST)


class WrittenImageContentShareView(APIView):
    def post(self, request, written_image_content_id):
        user_id = request.data.get("user_id")
        platform = request.data.get("platform", "Unknown")

        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserSession.objects.get(user_id=user_id)
            WrittenImageContentShare.objects.create(user=user, written_image_content_id=written_image_content_id, platform=platform)
            return Response({"message": "Share added successfully."}, status=status.HTTP_201_CREATED)
        except UserSession.DoesNotExist:
            return Response({"error": "User session not found."}, status=status.HTTP_400_BAD_REQUEST)



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
        user_id = request.data.get("user_id")
        text = request.data.get("text")

        if not user_id or not text:
            return Response({"error": "User ID and comment text are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserSession.objects.get(user_id=user_id)
            VideoContentComment.objects.create(user=user, video_content_id=video_content_id, text=text)
            return Response({"message": "Comment added successfully."}, status=status.HTTP_201_CREATED)
        except UserSession.DoesNotExist:
            return Response({"error": "User session not found."}, status=status.HTTP_400_BAD_REQUEST)


class VideoContentLikeView(APIView):
    def post(self, request, video_content_id):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserSession.objects.get(user_id=user_id)
            VideoContentLike.objects.create(user=user, video_content_id=video_content_id)
            return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
        except UserSession.DoesNotExist:
            return Response({"error": "User session not found."}, status=status.HTTP_400_BAD_REQUEST)

class VideoContentShareView(APIView):
    def post(self, request, video_content_id):
        user_id = request.data.get("user_id")
        platform = request.data.get("platform", "Unknown")

        if not user_id:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = UserSession.objects.get(user_id=user_id)
            VideoContentShare.objects.create(user=user, video_content_id=video_content_id, platform=platform)
            return Response({"message": "Share added successfully."}, status=status.HTTP_201_CREATED)
        except UserSession.DoesNotExist:
            return Response({"error": "User session not found."}, status=status.HTTP_400_BAD_REQUEST)
