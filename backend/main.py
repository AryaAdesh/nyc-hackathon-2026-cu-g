import asyncio
import json
import sys

# Import the Pydantic models and the endpoint functions directly from api.py
from api import (
    api_generate_concepts,
    api_expand_concepts,
    api_infuse_data,
    ConceptRequest,
    ExpandRequest,
    InfuseRequest
)

async def main():
    prompt = "A futuristic sci-fi city where humans and robots live in harmony, emphasizing scale, technology, and cinematic drama."
    
    # You can pass a custom prompt via command line arguments
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    
    print(f"========== STEP 1: GENERATE CONCEPTS ==========")
    print(f"Prompt: '{prompt}'")
    try:
        # Call the async endpoint function directly
        req1 = ConceptRequest(prompt=prompt)
        concepts = await api_generate_concepts(req1)
        print(f"Successfully generated {len(concepts)} concepts.\n")
    except Exception as e:
        print("Error generating concepts:", e)
        return
        
    print(f"========== STEP 2: EXPAND CONCEPTS ==========")
    try:
        req2 = ExpandRequest(concepts=concepts)
        expand_res = await api_expand_concepts(req2)
        raw_narrative = expand_res["raw_narrative"]
        print(f"Successfully expanded concepts. Narrative length: {len(raw_narrative)} characters.\n")
    except Exception as e:
        print("Error expanding concepts:", e)
        return
        
    print(f"========== STEP 3: INFUSE DATA ==========")
    try:
        req3 = InfuseRequest(raw_narrative=raw_narrative)
        infused_data = await api_infuse_data(req3)
        print("Successfully infused data. Final Output:\n")
        # Since infused_data is a Pydantic model (DataInfuserOutput), we can dump it to JSON
        print(infused_data.model_dump_json(indent=2))
    except Exception as e:
        print("Error infusing data:", e)
        return

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
    asyncio.run(main())
