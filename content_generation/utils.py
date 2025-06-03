import openai
from django.conf import settings

def generate_content_from_prompt(prompt_text, temperature=0.7, token_limit=256):
    """
    Calls OpenAI API to generate content based on a prompt.
    Returns a dict with title and body.
    """
    openai.api_key = settings.OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4.1",  # Use a model with search capability if needed
        messages=[
            {"role": "system", "content": "You are a helpful news generator."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=temperature,
        max_tokens=token_limit
    )
    content = response.choices[0].message.content.strip()
    # Split content: first sentence as title, rest as body
    parts = content.split('. ', 1)
    title = parts[0] + '.' if parts else 'Untitled'
    body = parts[1] if len(parts) > 1 else ''
    return {'title': title, 'body': body}
