import asyncio
import json
import sys
from pydantic import BaseModel

# Import the Pydantic models, endpoint functions, and app directly from api.py
from api import (
    app,
    api_generate_concepts,
    api_expand_concepts,
    api_infuse_data,
    api_generate_media,
    ConceptRequest,
    ExpandRequest,
    InfuseRequest,
    GenerateMediaRequest
)
from services.nano_banana import generate_image
from services.veo import generate_video

async def main():
    """
    Takes the transcribed audio prompt and orchestrates
    the entire pipeline (generate -> expand -> infuse -> media).
    """
    # You can pass a custom prompt via command line arguments
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        # Prompt user directly
        prompt = input("Please enter your prompt for the conceptual ad: ").strip()
        
        # Fallback if the user just hits enter without typing anything
        if not prompt:
            prompt = "A futuristic sci-fi city where humans and robots live in harmony, emphasizing scale, technology, and cinematic drama."
            print(f"No input detected. Using default prompt: '{prompt}'")
    
    print(f"========== STEP 1: GENERATE CONCEPTS ==========")
    print(f"Prompt: '{prompt}'")
    req1 = ConceptRequest(prompt=prompt)
    concepts = await api_generate_concepts(req1)
    print(f"Successfully generated {len(concepts)} concepts.\n")
    
    print(f"========== STEP 2: EXPAND CONCEPTS ==========")
    req2 = ExpandRequest(concepts=concepts)
    expand_res = await api_expand_concepts(req2)
    raw_narrative = expand_res["raw_narrative"]
    print(f"Successfully expanded concepts. Narrative length: {len(raw_narrative)} characters.\n")
    
    print(f"========== STEP 3: INFUSE DATA ==========")
    req3 = InfuseRequest(raw_narrative=raw_narrative)
    infused_data = await api_infuse_data(req3)
    print("Successfully infused data. Final Output derived.\n")
    
    print(f"========== STEP 4: GENERATE MEDIA ==========")
    stories_dicts = [story.model_dump() for story in infused_data.story_packages]
    req4 = GenerateMediaRequest(infused_stories=stories_dicts)
    final_output = await api_generate_media(req4)
    print("Successfully generated all media.\n")
    
    # Print the final result
    print("FINAL PIPELINE OUTPUT:")
    print(json.dumps(final_output, indent=2))
    
    return final_output

if __name__ == "__main__":
    asyncio.run(main())
