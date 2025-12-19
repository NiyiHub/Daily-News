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
            'evidence': <dict with structured evidence>,
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
        evidence = {}  # ✅ FIXED: Now returns dict instead of None/string
        verification_score = 0.0

        if 'claims' in data and data['claims']:
            # Get the first claimReview if available
            claim_reviews = data['claims'][0].get('claimReview', [])
            if claim_reviews:
                first_review = claim_reviews[0]
                textual_rating = first_review.get('textualRating', "Unverified")
                
                # ✅ FIXED: Structure evidence as object matching frontend expectations
                evidence = {
                    "url": first_review.get('url', ''),
                    "source": first_review.get('publisher', {}).get('name', 'Unknown Source'),
                    "summary": first_review.get('title', 'No summary available'),
                    "verification_status": textual_rating,
                    "supporting_documents": [
                        {
                            "url": first_review.get('url', ''),
                            "title": first_review.get('title', 'Source Document')
                        }
                    ] if first_review.get('url') else []
                }
                
                # Compute a simple verification score based on textual_rating
                rating_map = {
                    "TRUE": 1.0,
                    "True": 1.0,
                    "Mostly True": 0.8,
                    "Partly True": 0.5,
                    "Mostly False": 0.2,
                    "FALSE": 0.0,
                    "False": 0.0
                }
                verification_score = rating_map.get(textual_rating, 0.0)
                
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
            'evidence': {},  # ✅ Return empty dict on error
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
        evidence=result.get('evidence', {}),  # ✅ Now stores structured dict
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