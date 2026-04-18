import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import requests

# Load API keys from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="OpenVisualist AI Engine")

class EssayRequest(BaseModel):
    content: str

@app.get("/")
def read_root():
    return {"status": "OpenVisualist AI is Online", "version": "0.1.0-alpha"}

@app.post("/analyze")
async def analyze_essay(request: EssayRequest):
    """
    Step 1: The 'Brain' reads the essay and extracts visual keywords.
    """
    try:
        # AI logic to extract semantic visual cues
        response = openai.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a professional image archivist. Extract 3-5 high-quality visual search terms for public domain photos based on the user's text. Return only the terms separated by commas."},
                {"role": "user", "content": request.content}
            ]
        )
        
        keywords = response.choices[0].message.content.split(",")
        return {"keywords": [k.strip() for k in keywords]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/source")
async def source_images(query: str):
    """
    Step 2: The 'Librarian' searches Openverse for Public Domain matches.
    """
    # Placeholder for Openverse API logic
    # Documentation: https://api.openverse.org/
    openverse_url = f"https://api.openverse.org/v1/images/?q={query}&license_type=pdm,cc0"
    
    try:
        # In production, you'll need an Openverse Client ID
        # For now, we simulate the structure
        return {"query": query, "message": "Ready to connect to Openverse API", "results": []}
    except Exception as e:
        return {"error": str(e)}
