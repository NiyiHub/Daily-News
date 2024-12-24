from celery import shared_task
from .utils import generate_content
from .models import GeneratedContent

@shared_task
def generate_content_task(prompt, temperature=0.7, token_limit=256):
    result = generate_content(prompt, temperature, token_limit)
    GeneratedContent.objects.create(
        title="Generated Title",
        body=result['content'],
        prompt=prompt,
        temperature=temperature,
        token_limit=token_limit
    )
