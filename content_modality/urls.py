from django.urls import path 
from .views import (
    UserLoginView,
    UserSessionView,

    WrittenContentPostView, 
    WrittenContentGetView, 
    WrittenContentCommentView, 
    WrittenContentLikeView, 
    WrittenContentShareView,

    WrittenImageContentPostView, 
    WrittenImageContentGetView, 
    WrittenImageContentCommentView, 
    WrittenImageContentLikeView, 
    WrittenImageContentShareView,

    VideoContentPostView, 
    VideoContentGetView, 
    VideoContentCommentView, 
    VideoContentLikeView, 
    VideoContentShareView,

    UserBookmarkView,
    UserBookmarkView
)

urlpatterns = [
    path('api/user/login/', UserLoginView.as_view(), name='user-login'),
    path('api/user/session/', UserSessionView.as_view(), name='user-session'),
    
    # WrittenContent endpoints
    path('written/', WrittenContentPostView.as_view(), name='post_written_content'),
    path('written/get/', WrittenContentGetView.as_view(), name='get_written_content'),
    path('written/<int:written_content_id>/comment/', WrittenContentCommentView.as_view(), name='written_content_comment'),
    path('written/<int:written_content_id>/like/', WrittenContentLikeView.as_view(), name='written_content_like'),
    path('written/<int:written_content_id>/share/', WrittenContentShareView.as_view(), name='written_content_share'),
    
    # WrittenContent Bookmarking
    path('written/<int:written_content_id>/bookmark/', UserBookmarkView.as_view(), name='user_bookmark'),

    # WrittenImageContent endpoints
    path('written-image/', WrittenImageContentPostView.as_view(), name='post_written_image_content'),
    path('written-image/get/', WrittenImageContentGetView.as_view(), name='get_written_image_content'),
    path('written-image/<int:written_image_content_id>/comment/', WrittenImageContentCommentView.as_view(), name='written_image_content_comment'),
    path('written-image/<int:written_image_content_id>/like/', WrittenImageContentLikeView.as_view(), name='written_image_content_like'),
    path('written-image/<int:written_image_content_id>/share/', WrittenImageContentShareView.as_view(), name='written_image_content_share'),

    # WrittenImageContent Bookmarking
    path('written-image/<int:written_image_content_id>/bookmark/', UserBookmarkView.as_view(), name='user_bookmark'),

    # VideoContent endpoints
    path('video/', VideoContentPostView.as_view(), name='post_video_content'),
    path('video/get/', VideoContentGetView.as_view(), name='get_video_content'),
    path('video/<int:video_content_id>/comment/', VideoContentCommentView.as_view(), name='video_content_comment'),
    path('video/<int:video_content_id>/like/', VideoContentLikeView.as_view(), name='video_content_like'),
    path('video/<int:video_content_id>/share/', VideoContentShareView.as_view(), name='video_content_share'),

    # VideoContent Bookmarking
    path('video/<int:video_content_id>/bookmark/', UserBookmarkView.as_view(), name='user_bookmark'),

    # Retrieve all user bookmarks
    path('bookmarks/<str:user_id>/', UserBookmarkView.as_view(), name='get_user_bookmarks'),
]
