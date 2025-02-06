from django.urls import path
from .views import ProcessContentView

urlpatterns = [
    path('process/<int:content_id>/', ProcessContentView.as_view(), name='process_content'),
]
