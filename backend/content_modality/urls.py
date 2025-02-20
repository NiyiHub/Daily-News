from django.urls import path
from .views import CreateWrittenContentView, CreateWrittenImageContentView, CreateVideoContentView

urlpatterns = [
    path('written/', CreateWrittenContentView.as_view(), name='create_written_content'),
    path('written-image/', CreateWrittenImageContentView.as_view(), name='create_written_image_content'),
    path('video/', CreateVideoContentView.as_view(), name='create_video_content'),
]
