import os
import json
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import requests

# 1. SETUP - Loading the "Brain" and "Keys"
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENVERSE_CLIENT_ID = os.getenv("OPENVERSE_CLIENT_ID")
OPENVERSE_CLIENT_SECRET = os.getenv("OPENVERSE_CLIENT_SECRET")

app = FastAPI(title="OpenVisualist AI Engine")

# --- DATA MODELS ---

class EssayRequest(BaseModel):
    content: str

class ImageResult(BaseModel):
    url: str
    title: str
    creator: str
    license_url: str

# --- CORE LOGIC (THE GEARS) ---

def extract_keywords(text: str) -> List[str]:
    """
    Gear 1: The Analyst.
    Uses OpenAI to read the essay and extract visual metaphors/keywords.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a visual researcher. Extract 3-5 distinct, high-quality visual keywords for an image search based on the provided text. Return ONLY a comma-separated list."},
                {"role": "user", "content": text}
            ],
            max_tokens=50
        )
        keywords = response.choices[0].message.content.split(',')
        return [k.strip() for k in keywords]
    except Exception as e:
        print(f"Error in Analyst Gear: {e}")
        return []

def get_openverse_token():
    """
    Gear 2: The Credentialer.
    Authenticates with Openverse to get a temporary access token.
    """
    url = "https://api.openverse.org/v1/auth_tokens/token/"
    data = {
        'client_id': OPENVERSE_CLIENT_ID,
        'client_secret': OPENVERSE_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=data)
    return response.json().get('access_token')

def source_images(keyword: str, token: str) -> List[ImageResult]:
    """
    Gear 3: The Librarian.
    Broadened to find more results while still keeping things legal.
    """
    search_url = f"https://api.openverse.org/v1/images/?q={keyword}&page_size=1"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(search_url, headers=headers)
        print(f"Searching for {keyword}, Status: {response.status_code}")
        
        results = response.json().get('results', [])
        
        found_images = []
        for img in results:
            found_images.append(ImageResult(
                url=img.get('url'),
                title=img.get('title', 'Untitled'),
                creator=img.get('creator', 'Unknown'),
                license_url=img.get('license_url', 'https://creativecommons.org/')
            ))
        return found_images
    except Exception as e:
        print(f"Error in Librarian Gear: {e}")
        return []

# --- API ENDPOINTS ---

@app.post("/analyze-and-source", response_model=List[ImageResult])
async def process_essay(request: EssayRequest):
    """
    The Main Switch.
    Combines all gears to turn an essay into a gallery.
    """
    if not request.content:
        raise HTTPException(status_code=400, detail="Essay content is empty.")

    # Step 1: Analyze keywords
    keywords = extract_keywords(request.content)
    
    # Step 2: Get Auth
    token = get_openverse_token()
    
    # Step 3: Source images for each keyword
    all_images = []
    for kw in keywords:
        images = source_images(kw, token)
        all_images.extend(images)
    
    return all_images

@app.get("/")
def health_check():
    return {"status": "OpenVisualist AI Engine is humming."}

