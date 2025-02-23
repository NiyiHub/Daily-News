from django.urls import path
from .views import (
    WrittenContentPostView, 
    WrittenContentGetView,
    WrittenImageContentPostView, 
    WrittenImageContentGetView,
    VideoContentPostView, 
    VideoContentGetView
)

urlpatterns = [
    # Endpoints for Written Content
    path('written/', WrittenContentPostView.as_view(), name='post_written_content'),
    path('written/get/', WrittenContentGetView.as_view(), name='get_written_content'),
    
    # Endpoints for Written+Image Content
    path('written-image/', WrittenImageContentPostView.as_view(), name='post_written_image_content'),
    path('written-image/get/', WrittenImageContentGetView.as_view(), name='get_written_image_content'),
    
    # Endpoints for Video Content
    path('video/', VideoContentPostView.as_view(), name='post_video_content'),
    path('video/get/', VideoContentGetView.as_view(), name='get_video_content'),
]
