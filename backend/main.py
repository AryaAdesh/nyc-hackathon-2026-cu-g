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
    infuser = DataInfuser(client.models)
    
    # Needs to be awaited
    result = await infuser.infuse_data(req.raw_narrative)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
