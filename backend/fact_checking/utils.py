import requests
from django.conf import settings

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
    Query a general news API (e.g., NewsAPI.org) for related articles.
    """
    endpoint = "https://newsapi.org/v2/everything"
    headers = {
        "Authorization": f"Bearer {settings.NEWS_API_KEY}"
    }
    params = {
        "q": claim,
        "sortBy": "relevancy",
        "pageSize": 5
    }
    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if 'articles' in data and data['articles']:
        evidence = [article['url'] for article in data['articles'][:3]]
        return {"status": "Unverified", "evidence": evidence}
    return {"status": "Unverified", "evidence": None}
