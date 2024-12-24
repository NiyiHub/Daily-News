from django.urls import path
from .views import ContentGenerationView

urlpatterns = [
    path('generate/', ContentGenerationView.as_view(), name='generate_content'),
]
