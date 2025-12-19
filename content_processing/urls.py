from django.urls import path
from .views import (
    ProcessContentView, 
    PublishedContentEvidenceView, 
    CategoryDetailView,
    NewsArticleEvidenceView  # ✅ NEW IMPORT
)

urlpatterns = [
    path('process/<int:content_id>/', ProcessContentView.as_view(), name='process_content'),
    
    # Old endpoint - kept for backward compatibility
    path('published/<int:published_content_id>/evidence/', PublishedContentEvidenceView.as_view(), name='published_content_evidence'),
    
    # ✅ NEW ENDPOINT: Get evidence by news article ID
    path('news/<int:news_id>/evidence/', NewsArticleEvidenceView.as_view(), name='news_article_evidence'),
    
    path('categories/<int:processed_content_id>/', CategoryDetailView.as_view(), name='category_detail'),
]