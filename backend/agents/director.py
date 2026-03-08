from pydantic import BaseModel, Field
import json
from google import genai
from google.genai import types
from .prompt_templates import DIRECTOR_SYSTEM_PROMPT

class AdConcept(BaseModel):
    id: int = Field(description="Concept number: 1 (Scientific), 2 (Abstract), or 3 (Cinematic)")
    title: str = Field(description="Punchy 2-4 word concept title. Evocative, not descriptive.")
    subtitle: str = Field(description="One sentence (max 10 words) naming the aesthetic world.")
    lensType: str = Field(description="Exactly one of: Scientific, Abstract, or Cinematic")
    nanoBananaPrompt: str = Field(description="Highly detailed hero image generation prompt following the SUBJECT+ENVIRONMENT+LIGHTING+CAMERA+MOOD+TECHNICAL structure. Must end with '8K ultra-detailed, shot on Hasselblad, cinematic color grade'.")
    veoPrompt: str = Field(description="5-8 second loopable ambient video scene: OPENING FRAME + CAMERA MOVEMENT + ATMOSPHERE + ENDING BEAT. One continuous shot, no hard cuts.")
    narrationScript: str = Field(description="15-25 seconds of spoken narration (40-65 words) matched to the lens tone. Ends with a standalone tagline on its own line formatted as: — [TAGLINE]")

def generate_concepts(user_prompt: str) -> list[dict]:
    """
    Takes a user voice transcript/prompt, hits Gemini 2.0 Flash, and returns
    a JSON array of exactly 3 ad concepts to populate the 3D tunnel nodes.
    """
    client = genai.Client()  # Assumes GEMINI_API_KEY is in environment

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=DIRECTOR_SYSTEM_PROMPT,
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
