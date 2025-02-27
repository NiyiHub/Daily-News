from celery import shared_task
from .utils import generate_content_from_prompt
from .models import APIPrompt, GeneratedContent

@shared_task
def generate_content_task(prompt_text, temperature=0.7, token_limit=256):
    """
    Celery task to generate content from a given prompt.
    It creates an APIPrompt record, calls the OpenAI API, and saves the generated content
    linked to the APIPrompt.
    """
    # Create an APIPrompt record to store the prompt details.
    prompt_obj = APIPrompt.objects.create(
        prompt_text=prompt_text,
        temperature=temperature,
        token_limit=token_limit,
        status='pending'
    )
    
    try:
        # Generate content using the OpenAI API.
        result = generate_content_from_prompt(prompt_text, temperature=temperature, token_limit=token_limit)
        # Create a GeneratedContent record, linking it to the prompt.
        GeneratedContent.objects.create(
            prompt=prompt_obj,
            title=result.get('title', 'Untitled'),
            body=result.get('body', '')
        )
        # Update the prompt status on success.
        prompt_obj.status = 'completed'
        prompt_obj.save()
    except Exception as e:
        # Update status to error if an exception occurs.
        prompt_obj.status = 'error'
        prompt_obj.save()
        raise e
