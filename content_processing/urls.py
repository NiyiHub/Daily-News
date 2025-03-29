from django.urls import path
from .views import ProcessContentView,PublishedContentEvidenceView, CategoryListView

urlpatterns = [
    path('process/<int:content_id>/', ProcessContentView.as_view(), name='process_content'),
    path('published/<int:published_content_id>/evidence/', PublishedContentEvidenceView.as_view(), name='published_content_evidence'),
    path('categories/', CategoryListView.as_view(), name='category_list'),

]
