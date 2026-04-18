# A conceptual snippet for your engine.py
import openai
import requests

def get_visual_cues(essay_text):
    """Uses AI to turn an essay into specific search queries."""
    prompt = f"Analyze this text and provide 3 specific visual search terms for public domain photos: {essay_text}"
    # AI logic here...
    return ["vintage typewriter", "dusty library", "mechanical keys"]

def source_from_openverse(query):
    """Queries the Openverse API for CC0/Public Domain images."""
    url = f"https://api.openverse.org/v1/images/?q={query}&license_type=pdm,cc0"
    response = requests.get(url)
    return response.json()['results']
