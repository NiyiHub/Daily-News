import requests
from django.conf import settings
from .models import FactCheckResult

def query_google_fact_check(claim):
    """
    Query Google Fact Check Explorer API and return evidence and a score for accuracy.
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
        if 'claims' in data and data['claims']:
            return {"accuracy": 0.9, "evidence": data['claims'][0].get('claimReview', [{}])[0].get('url', "")}
    except Exception as e:
        print("Google Fact Check API error:", e)
    return {"accuracy": 0.5, "evidence": None}

def query_news_api(claim):
    """
    Query NewsAPI for articles related to the claim and return evidence and a source score.
    """
    endpoint = "https://newsapi.org/v2/everything"
    headers = {"Authorization": f"Bearer {settings.NEWS_API_KEY}"}
    # Use a simple keyword extraction (could be replaced with a more robust method)
    query_string = claim[:50]
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
    Process fact-checking for a GeneratedContent instance.
    Evaluate the claim based on Disclosure, Source, Accuracy, and Clarity.
    Store evidence from external APIs and compute a composite score.
    """
    claim = generated_content.body
    # For demonstration, dummy scores for Disclosure and Clarity are now placeholders.
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
    Returns a FactCheckResult instance.
    """
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
