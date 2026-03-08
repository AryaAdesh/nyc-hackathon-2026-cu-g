from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from agents.director import generate_concepts
from services.nano_banana import generate_image
from services.veo import generate_video

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

@app.post("/api/generate-concepts")
async def api_generate_concepts(req: ConceptRequest):
    """
    Takes user voice transcript, hits Gemini 1.5 Pro to generate 3 concepts,
    then sequentially generates images and videos for each concept,
    returning the fully populated JSON array.
    """
    concepts = generate_concepts(req.prompt)
    
    # Sequentially populate assets
    for concept in concepts:
        # Generate and append media URLs
        concept["imageUrl"] = generate_image(concept.get("nanoBananaPrompt", ""))
        concept["videoUrl"] = generate_video(concept.get("veoPrompt", ""))
        
    return concepts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
