import requests
from django.conf import settings

import spacy
from collections import Counter
import re

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text, num_keywords=5):
    """
    Extract key phrases or keywords from a given text using spaCy.

    Args:
        text (str): The input story or claim text.
        num_keywords (int): The number of top keywords to return (default: 5).

    Returns:
        list: A list of extracted keywords.
    """
    # Preprocess the text
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    doc = nlp(text)

    # Extract proper nouns, named entities, and frequent terms
    proper_nouns = [token.text for token in doc if token.pos_ in ["PROPN", "NOUN"]]
    named_entities = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "ORG", "PERSON", "EVENT", "DATE"]]
    
    # Combine all potential keywords
    all_keywords = proper_nouns + named_entities

    # Count frequencies and get the most common keywords
    keyword_counts = Counter(all_keywords)
    top_keywords = [keyword for keyword, _ in keyword_counts.most_common(num_keywords)]

    return top_keywords


def query_google_fact_check(claim):
    """
    Query Google Fact Check Explorer API with a claim.
    """
    endpoint = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {
        "query": claim,
        "key": settings.GOOGLE_FACT_CHECK_API_KEY
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    data = response.json()

    if 'claims' in data and data['claims']:
        return {
            "status": "Verified" if data['claims'][0]['claimReview'][0]['textualRating'] == "TRUE" else "False",
            "evidence": data['claims'][0]['claimReview'][0]['url']
        }
    return {"status": "Unverified", "evidence": None}


def query_news_api(claim):
    """
    Query the News API with concise keywords extracted from the claim.
    """
    endpoint = "https://newsapi.org/v2/everything"
    headers = {
        "Authorization": f"Bearer {settings.NEWS_API_KEY}"
    }

    # Dynamically extract keywords from the claim
    keywords = extract_keywords(claim)
    query_string = " OR ".join(keywords)  # Create a query string with OR between keywords

    params = {
        "q": query_string,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 5
    }

    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for non-2xx responses
    data = response.json()

    if 'articles' in data and data['articles']:
        evidence = [article['url'] for article in data['articles'][:3]]
        return {"status": "Unverified", "evidence": evidence}
    return {"status": "Unverified", "evidence": None}


