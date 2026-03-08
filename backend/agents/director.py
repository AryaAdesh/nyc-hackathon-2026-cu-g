from pydantic import BaseModel, Field
import json
from google import genai
from google.genai import types

class AdConcept(BaseModel):
    id: int = Field(description="Unique ID for the concept (1, 2, or 3)")
    title: str = Field(description="Punchy title")
    subtitle: str = Field(description="Short description")
    lensType: str = Field(description="Scientific, Abstract, or Cinematic")
    nanoBananaPrompt: str = Field(description="Highly detailed 4k cinematic image prompt")
    veoPrompt: str = Field(description="Slow panning ambient background video prompt")
    narrationScript: str = Field(description="Live narration script to be spoken over the visuals")

def generate_concepts(user_prompt: str) -> list[dict]:
    """
    Takes a user voice transcript/prompt, hits Gemini 1.5 Pro, and returns
    a JSON array of exactly 3 ad concepts to populate the 3D tunnel text.
    """
    client = genai.Client() # Assumes GEMINI_API_KEY is in environment
    
    system_instruction = """You are the Director Agent for the 'COSMIC STAGE' AD GENERATION PLATFORM.
You take a short spoken user prompt and expand it into exactly three distinct, highly detailed advertising concepts:
1. Path Alpha (Scientific): Hyper-realistic, data-driven visualization.
2. Path Beta (Abstract): Vibe-driven, metaphorical, emotional.
3. Path Gamma (Cinematic): Dramatic, story-driven world-building.

Return exactly 3 concepts, each mapping to one of these paths.
"""
    
    response = client.models.generate_content(
        model='gemini-1.5-pro',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            response_schema=list[AdConcept],
            temperature=0.7,
        )
    )
    
    # Extract the results
    try:
        # If the SDK automatically parses the response via `parsed`
        if getattr(response, "parsed", None):
            return [concept.model_dump() for concept in response.parsed]
        # Otherwise fallback to parsing the JSON text manually
        return json.loads(response.text)
    except Exception as e:
        print(f"Error parsing model response: {e}")
        return []
