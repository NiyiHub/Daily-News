import openai
from django.conf import settings

# Initialize OpenAI API key (set via environment variables for security)
openai.api_key = settings.OPENAI_API_KEY

def generate_content(prompt, temperature=0.7, token_limit=256):
    """
    Sends a prompt to the LLM and retrieves the generated story.
    
    Args:
        prompt (str): The narrative prompt to send to the LLM.
        temperature (float): Controls randomness in output (default: 0.7).
        token_limit (int): The maximum number of tokens in the output (default: 256).
    
    Returns:
        dict: Generated content and metadata.
    """
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # Specify the LLM engine
        prompt=prompt,
        max_tokens=token_limit,
        temperature=temperature
    )
    return {
        'content': response['choices'][0]['text'].strip(),
        'metadata': {
            'temperature': temperature,
            'token_limit': token_limit
        }
    }

