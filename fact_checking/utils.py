import requests
from django.conf import settings
from .models import FactCheckResult

def query_google_fact_check(claim):
    """
    Query the Google Fact Check Explorer API using the given claim.
    Process the response to extract the textual rating, evidence, and compute a verification score.
    
    Returns:
        dict: {
            'textual_rating': <str>,
            'evidence': <evidence details (e.g., URL or list of URLs)>,
            'verification_score': <float>
        }
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

        # Default values if no claims found
        textual_rating = "Unverified"
        evidence = None
        verification_score = 0.0

        if 'claims' in data and data['claims']:
            # Get the first claimReview if available
            claim_reviews = data['claims'][0].get('claimReview', [])
            if claim_reviews:
                textual_rating = claim_reviews[0].get('textualRating', "Unverified")
                # Compute a simple verification score based on textual_rating
                # For example: "TRUE" -> 1.0, "Mostly True" -> 0.8, "Mostly False" -> 0.2, "FALSE" -> 0.0
                rating_map = {
                    "TRUE": 1.0,
                    "Mostly True": 0.8,
                    "Partly True": 0.5,
                    "Mostly False": 0.2,
                    "FALSE": 0.0
                }
                verification_score = rating_map.get(textual_rating, 0.0)
                evidence = claim_reviews[0].get('url', "")
        return {
            'textual_rating': textual_rating,
            'evidence': evidence,
            'verification_score': verification_score
        }
    except Exception as e:
        # Log or print the error as needed
        print("Google Fact Check API error:", e)
        return {
            'textual_rating': "Error",
            'evidence': None,
            'verification_score': 0.0
        }

def process_fact_check_manual(claim):
    """
    Manually process fact checking for a provided claim.
    Uses the Google Fact Check API to evaluate the claim and creates a FactCheckResult record.
    
    Returns:
        FactCheckResult instance.
    """
    result = query_google_fact_check(claim)
    fact_check_result = FactCheckResult.objects.create(
        claim=claim,
        textual_rating=result.get('textual_rating', "Unverified"),
        evidence=result.get('evidence'),
        verification_score=result.get('verification_score', 0.0)
    )
    return fact_check_result

def process_fact_check_for_content(generated_content):
    """
    Automatically process fact checking for a GeneratedContent instance.
    Uses the generated content's body as the claim.
    """
    claim = generated_content.body
    process_fact_check_manual(claim)
