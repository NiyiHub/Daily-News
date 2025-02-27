import spacy
import re
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def categorize_content(text):
    """
    Dynamically categorize content based on predefined keyword mappings.
    Returns a list of relevant categories.
    """
    categories_keywords = {
        "AI": ["artificial intelligence", "machine learning", "deep learning", "AI"],
        "Technology": ["technology", "gadgets", "innovation", "tech"],
        "Gadgets": ["smartphone", "tablet", "laptop", "gadget"],
        "Politics": ["government", "election", "policy", "politics"],
        "Health": ["medicine", "health", "wellness", "disease"],
        "Environment": ["climate", "environment", "sustainability"]
    }
    text_clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', text).lower()
    doc = nlp(text_clean)
    tokens = [token.text for token in doc]
    matched_categories = []
    for category, keywords in categories_keywords.items():
        for keyword in keywords:
            if keyword.lower() in tokens:
                matched_categories.append(category)
                break
    return list(set(matched_categories)) if matched_categories else ["General"]

def tag_content(text):
    """
    Extract tags from text using spaCy named entity recognition.
    Returns a list of unique tags (up to 10).
    """
    doc = nlp(text)
    tags = [ent.text for ent in doc.ents]
    unique_tags = list(dict.fromkeys(tags))
    return unique_tags[:10]

def process_generated_content(generated_instance):
    """
    Process a GeneratedContent instance:
      - Categorize the content.
      - Extract tags.
      - Create a ProcessedContent record.
    This function is triggered automatically via a post_save signal in content_generation.
    """
    from .models import ProcessedContent  # Import here to avoid circular dependencies
    categories = categorize_content(generated_instance.body)
    tags = tag_content(generated_instance.body)
    # Create ProcessedContent; fact-check data and publish_status will be computed in its save() method.
    ProcessedContent.objects.create(
        content=generated_instance,
        categories=categories,
        tags=tags
    )
