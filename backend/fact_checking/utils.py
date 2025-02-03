import requests
from django.conf import settings
from .models import FactCheckResult

# import spacy
# from collections import Counter
# import re

# # Load the spaCy language model
# nlp = spacy.load("en_core_web_sm")

# def extract_keywords(text, num_keywords=5):
#     """
#     Extract key phrases or keywords from a given text using spaCy.

#     Args:
#         text (str): The input story or claim text.
#         num_keywords (int): The number of top keywords to return (default: 5).

#     Returns:
#         list: A list of extracted keywords.
#     """
#     # Preprocess the text
#     text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
#     doc = nlp(text)

#     # Extract proper nouns, named entities, and frequent terms
#     proper_nouns = [token.text for token in doc if token.pos_ in ["PROPN", "NOUN"]]
#     named_entities = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "ORG", "PERSON", "EVENT", "DATE"]]
    
#     # Combine all potential keywords
#     all_keywords = proper_nouns + named_entities

#     # Count frequencies and get the most common keywords
#     keyword_counts = Counter(all_keywords)
#     top_keywords = [keyword for keyword, _ in keyword_counts.most_common(num_keywords)]

#     return top_keywords


# fact_checking/utils.py 

def query_google_fact_check(claim):
    """
    Query the Google Fact Check Explorer API for the claim.
    Returns a dictionary with evidence and a dummy score for demonstration.
    """
    endpoint = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {
        "query": claim,
        "key": settings.GOOGLE_FACT_CHECK_API_KEY
    }
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()
        # Dummy scoring logic for demonstration:
        if 'claims' in data and data['claims']:
            # Assume a verified claim gets a high score in accuracy.
            return {"accuracy": 0.9, "evidence": data['claims'][0].get('claimReview', [{}])[0].get('url', "")}
    except Exception as e:
        print("Google Fact Check API error:", e)
    return {"accuracy": 0.5, "evidence": None}

def query_news_api(claim):
    """
    Query NewsAPI for articles related to the claim.
    Returns a dictionary with dummy scores and evidence URLs.
    """
    endpoint = "https://newsapi.org/v2/everything"
    headers = {
        "Authorization": f"Bearer {settings.NEWS_API_KEY}"
    }
    # For a better query, extract keywords (use a helper function; see content_processing/utils.py)
    query_string = claim[:50]  # Simple approach: use first 50 characters as query (improve with NLP later)
    params = {
        "q": query_string,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 5
    }
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if 'articles' in data and data['articles']:
            evidence_urls = [article['url'] for article in data['articles'][:3]]
            return {"source": 0.8, "evidence": evidence_urls}
    except Exception as e:
        print("News API error:", e)
    return {"source": 0.5, "evidence": None}

def process_fact_check_for_content(generated_content):
    """
    Process fact checking for a given GeneratedContent instance.
    Uses multiple APIs to evaluate the claim based on criteria.
    Sets dummy scores for Disclosure, Source Identification, Accuracy, and Clarity.
    Stores a composite score.
    """
    claim = generated_content.body  # We use the body as the claim

    # For demonstration, we set dummy scores for disclosure and clarity.
    disclosure_score = 0.8  # Assume content has decent disclosure
    clarity_score = 0.85    # Assume content is clear

    # Query external APIs for additional criteria
    google_result = query_google_fact_check(claim)
    news_result = query_news_api(claim)

    accuracy_score = google_result.get("accuracy", 0.5)
    source_score = news_result.get("source", 0.5)

    # Compute a composite score as a weighted average
    # For example: weights: disclosure: 0.25, source: 0.25, accuracy: 0.25, clarity: 0.25
    composite_score = (disclosure_score + source_score + accuracy_score + clarity_score) / 4.0

    # Store evidence details
    details = {
        "google_evidence": google_result.get("evidence"),
        "news_evidence": news_result.get("evidence")
    }

    # Create a FactCheckResult entry
    FactCheckResult.objects.create(
        claim=claim,
        disclosure_score=disclosure_score,
        source_score=source_score,
        accuracy_score=accuracy_score,
        clarity_score=clarity_score,
        composite_score=composite_score,
        details=details
    )

def process_fact_check_manual(claim):
    """
    Manually process fact checking for a provided claim.
    (This function can be used by the DRF view for manual fact-checking.)
    """
    # Similar logic to process_fact_check_for_content, but without a GeneratedContent instance.
    disclosure_score = 0.8
    clarity_score = 0.85

    google_result = query_google_fact_check(claim)
    news_result = query_news_api(claim)

    accuracy_score = google_result.get("accuracy", 0.5)
    source_score = news_result.get("source", 0.5)

    composite_score = (disclosure_score + source_score + accuracy_score + clarity_score) / 4.0
    details = {
        "google_evidence": google_result.get("evidence"),
        "news_evidence": news_result.get("evidence")
    }

    result = FactCheckResult.objects.create(
        claim=claim,
        disclosure_score=disclosure_score,
        source_score=source_score,
        accuracy_score=accuracy_score,
        clarity_score=clarity_score,
        composite_score=composite_score,
        details=details
    )
    return result



