import os
import urllib.parse
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import requests

# 1. INITIALIZATION & KEYS
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENVERSE_CLIENT_ID = os.getenv("OPENVERSE_CLIENT_ID")
OPENVERSE_CLIENT_SECRET = os.getenv("OPENVERSE_CLIENT_SECRET")

app = FastAPI(title="OpenVisualist AI Engine")

# 2. SECURITY (CORS) - Allows your website to talk to Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATA MODELS ---

class EssayRequest(BaseModel):
    content: str

class ImageResult(BaseModel):
    url: str
    title: str
    creator: str
    license_url: str

# --- THE GEARS (LOGIC) ---

def get_openverse_token():
    """Requests a fresh access token from Openverse."""
    url = "https://api.openverse.org/v1/auth_tokens/token/"
    data = {
        'client_id': OPENVERSE_CLIENT_ID,
        'client_secret': OPENVERSE_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    try:
        response = requests.post(url, data=data)
        token = response.json().get('access_token')
        if not token:
            print(f"CRITICAL: Token request failed. Response: {response.text}")
        return token
    except Exception as e:
        print(f"TOKEN GEAR ERROR: {e}")
        return None

def source_images(keyword: str, token: str) -> List[ImageResult]:
    """Searches Openverse for a specific keyword using a valid token."""
    if not token:
        return []

    # Clean keyword and make it URL-safe (e.g., "Jazz Music" -> "Jazz%20Music")
    clean_kw = keyword.replace("[", "").replace("]", "").replace('"', "").strip()
    encoded_kw = urllib.parse.quote(clean_kw)
    
    # We use a broad search first to ensure we get results
    search_url = f"https://api.openverse.org/v1/images/?q={encoded_kw}&page_size=3"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(search_url, headers=headers)
        # Check logs in Render to see if this is 200, 401, or 403
        print(f"LIBRARIAN LOG [{clean_kw}]: Status {response.status_code}")
        
        data = response.json()
        results = data.get('results', [])
        
        found_images = []
        for img in results:
            found_images.append(ImageResult(
                url=img.get('url'),
                title=img.get('title', 'Untitled Archive Piece'),
                creator=img.get('creator', 'Public Domain Source'),
                license_url=img.get('license_url', 'https://creativecommons.org/')
            ))
        return found_images
    except Exception as e:
        print(f"LIBRARIAN GEAR ERROR: {e}")
        return []

# --- THE MAIN ENDPOINT ---

@app.post("/analyze-and-source", response_model=List[ImageResult])
async def process_essay(request: EssayRequest):
    """The master switch that connects the Essay to the Gallery."""
    if not request.content:
        raise HTTPException(status_code=400, detail="Essay content cannot be empty.")

    # STEP 1: Extract Keywords via OpenAI
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a researcher. Extract 3-5 simple, concrete visual nouns from the text as a comma-separated list. No extra text."},
                {"role": "user", "content": request.content}
            ],
            max_tokens=60
        )
        raw_keywords = response.choices[0].message.content
        keywords = [k.strip() for k in raw_keywords.split(',')]
        print(f"ANALYST GEAR: Extracted {keywords}")
    except Exception as e:
        print(f"ANALYST GEAR ERROR: {e}")
        return []

    # STEP 2: Get Auth Token Once
    token = get_openverse_token()
    if not token:
        return []

    # STEP 3: Source Images
    all_results = []
    for kw in keywords:
        images = source_images(kw, token)
        all_results.extend(images)
    
    # Return the final JSON list to the frontend
    return all_results

@app.get("/")
def health_check():
    return {"status": "OpenVisualist AI Engine is humming."}
