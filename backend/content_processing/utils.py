import spacy
import re
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def categorize_content(text):
    """
    Categorize content by extracting keywords and matching them to predefined categories.
    Returns a list of categories.
    """
    # Predefined mapping of keywords to categories
    categories_keywords = {
        "AI": ["artificial intelligence", "machine learning", "deep learning", "AI"],
        "Technology": ["technology", "gadgets", "innovation", "tech"],
        "Gadgets": ["smartphone", "tablet", "laptop", "gadget"],
        "Politics": ["government", "election", "policy", "politics"],
        "Health": ["medicine", "health", "wellness", "disease"],
        "Environment": ["climate", "environment", "sustainability"]
    }

    # Clean and lower the text
    text_clean = re.sub(r'[^a-zA-Z0-9\s]', ' ', text).lower()

    # Tokenize text using spaCy
    doc = nlp(text_clean)
    tokens = [token.text for token in doc]

    # Count token frequencies
    token_counts = Counter(tokens)

    matched_categories = []
    for category, keywords in categories_keywords.items():
        # If any keyword appears in the tokens, add the category
        for keyword in keywords:
            if keyword.lower() in tokens:
                matched_categories.append(category)
                break  # No need to check other keywords for this category

    # Ensure uniqueness
    return list(set(matched_categories)) if matched_categories else ["General"]

def tag_content(text):
    """
    Extract tags from the text based on named entities using spaCy.
    Returns a list of tags.
    """
    doc = nlp(text)
    tags = [ent.text for ent in doc.ents]
    # Return unique tags and limit to a reasonable number, e.g., top 10
    unique_tags = list(dict.fromkeys(tags))
    return unique_tags[:10]
