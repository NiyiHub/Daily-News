import spacy

nlp = spacy.load("en_core_web_sm")

def categorize_content(content):
    """
    Categorize content based on keywords and context.
    Each piece of content is categorized into multiple relevant categories.
    """
    # Define predefined categories and keywords
    categories_keywords = {
        "AI": ["artificial intelligence", "AI", "machine learning"],
        "Technology": ["technology", "gadgets", "innovation"],
        "Politics": ["government", "policy", "elections", "politics"],
        "Health": ["medicine", "health", "wellness", "disease"],
        "Environment": ["climate", "environment", "sustainability"]
    }

    # Tokenize the content and normalize it
    doc = nlp(content.lower())
    tokens = [token.text for token in doc]

    # Determine categories based on matching keywords
    matched_categories = []
    for category, keywords in categories_keywords.items():
        if any(keyword in tokens for keyword in keywords):
            matched_categories.append(category)

    # Fallback category if no match
    if not matched_categories:
        matched_categories.append("General")

    return matched_categories
