from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents.director import generate_concepts, AdConcept
from agents.expander import expand_concepts
from agents.data_infuser import DataInfuser
from agents.infuser_schema import DataInfuserOutput
from google import genai

app = FastAPI(title="Cosmic Stage Ad Agency API")

# Add CORS middleware for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConceptRequest(BaseModel):
    prompt: str

class ExpandRequest(BaseModel):
    concepts: list[dict]

class InfuseRequest(BaseModel):
    raw_narrative: str

@app.post("/api/generate-concepts")
async def api_generate_concepts(req: ConceptRequest):
    """
    Takes user voice transcript, hits Gemini 1.5 Pro to generate exactly 3 concepts.
    Returns the JSON array without generating images/videos.
    """
    concepts = generate_concepts(req.prompt)
    return concepts

@app.post("/api/expand-concepts")
async def api_expand_concepts(req: ExpandRequest):
    """
    Takes 3 concepts and expands them into a raw narrative string.
    """
    raw_narrative = expand_concepts(req.concepts)
    return {"raw_narrative": raw_narrative}

@app.post("/api/infuse-data", response_model=DataInfuserOutput)
async def api_infuse_data(req: InfuseRequest):
    """
    Takes the expanded raw narrative and infuses it into a strict JSON format 
    ready for image and video generation APIs.
    """
    # Assuming GEMINI_API_KEY is set in environment
    client = genai.Client()
    infuser = DataInfuser(client.aio.models)
    
    # Needs to be awaited
    result = await infuser.infuse_data(req.raw_narrative)
    return result

class GenerateMediaRequest(BaseModel):
    infused_stories: list[dict]

from services.nano_banana import generate_image
from services.veo import generate_video

@app.post("/api/generate-media")
async def api_generate_media(req: GenerateMediaRequest):
    """
    Takes the properly infused stories (with Nano Banana and Veo prompts)
    and sequentially calls the image and video generation APIs.
    """
    stories = req.infused_stories
    
    for story in stories:
        # We process sequentially to avoid aggressive rate limits
        print(f"Generating media for: {story.get('title', 'Unknown Title')}")
        
        # 1. Generate Image
        image_prompt = story.get("nano_banana_prompt", "")
        if image_prompt:
            story["imageUrl"] = await generate_image(image_prompt)
        
        # 2. Generate Video
        video_prompt = story.get("veo_prompt", "")
        if video_prompt:
            story["videoUrl"] = await generate_video(video_prompt)
            
    return {"stories": stories}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
