import spacy
import re
from collections import Counter
from django.db import transaction
from .models import ProcessedContent, PublishedContent
from fact_checking.models import FactCheckResult

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
      - Automatically create PublishedContent if fact_check_status is "unverified"
    
    Note: This function is called by a signal from content_generation app.
    The signal in models.py (trigger_publication) will also try to create PublishedContent,
    so we use get_or_create to prevent duplicates.
    """
    try:
        with transaction.atomic():
            print(f"[PROCESS] Starting processing for: {generated_instance.title} (ID: {generated_instance.id})")

            # Check if already processed to avoid duplicates
            if hasattr(generated_instance, 'processed_content'):
                print(f"[PROCESS] Content already processed, skipping...")
                return generated_instance.processed_content

            # Categorize and tag the content
            categories = categorize_content(generated_instance.body)
            tags = tag_content(generated_instance.body)
            print(f"[PROCESS] Categories: {categories}, Tags: {tags[:3]}...")

            # Look for fact check result
            fact_check = FactCheckResult.objects.filter(claim=generated_instance.body).first()
            
            if fact_check:
                print(f"[PROCESS] Fact check found: {fact_check.textual_rating}")
                fact_check_status = fact_check.textual_rating
                composite_score = fact_check.verification_score
                evidence = fact_check.evidence if fact_check.evidence else {}
            else:
                print(f"[PROCESS] No fact check found, defaulting to Unverified")
                fact_check_status = "Unverified"
                composite_score = 0.0
                evidence = {}

            # Create ProcessedContent
            # Note: The save() method in ProcessedContent model will also fetch fact_check
            # and set publish_status, but we're being explicit here
            processed = ProcessedContent.objects.create(
                content=generated_instance,
                categories=categories,
                tags=tags,
                # These will be overridden by the save() method, but setting them anyway
                fact_check_status=fact_check_status,
                composite_score=composite_score,
                evidence=evidence
            )
            print(f"[PROCESS] ProcessedContent created (ID: {processed.id})")
            print(f"[PROCESS] Publish status: {processed.publish_status}")

            # The post_save signal (trigger_publication) in models.py will handle
            # PublishedContent creation, so we DON'T create it here to avoid duplicates
            # If for some reason you want to ensure it's created, use get_or_create:
            
            if processed.fact_check_status.lower() == "unverified":
                published, created = PublishedContent.objects.get_or_create(
                    processed_content=processed,
                    defaults={
                        "title": generated_instance.title,
                        "body": generated_instance.body,
                        "fact_check_status": processed.fact_check_status,
                        "evidence": processed.evidence,
                        "tags": processed.tags
                    }
                )
                if created:
                    print(f"[PROCESS] PublishedContent created (ID: {published.id})")
                else:
                    print(f"[PROCESS] PublishedContent already exists (ID: {published.id})")
            else:
                print(f"[PROCESS] Content withheld from publication (status: {processed.fact_check_status})")

            print(f"[PROCESS] Processing complete for article ID {generated_instance.id}")
            return processed

    except Exception as e:
        print(f"[PROCESS ERROR] Failed to process content: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise  # Re-raise to see the full error in logs