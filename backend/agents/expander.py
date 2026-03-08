from google import genai
import json

def expand_concepts(concepts: list[dict]) -> str:
    """
    Takes the 3 generated ad concepts and expands them into a unified,
    detailed raw narrative string to be used for video/image generation data extraction.
    """
    client = genai.Client() # Assumes GEMINI_API_KEY is in environment
    
    system_instruction = """You are the Expander Agent for the 'COSMIC STAGE' AD GENERATION PLATFORM.
Given 3 distinct ad concepts, your job is to write a highly detailed, continuous raw narrative that elaborates on all 3 concepts.
For each concept, expand on:
1. The visual flow of the video, focusing heavily on camera movement and temporal changes.
2. The specific visual textures, lighting, and overarching art style.
3. The tone of the voiceover that will accompany it.

Format your output as a continuous plain text narrative without markdown formatting. Do not use JSON. Make it evocative and extremely detailed.
"""
    
    # Convert concepts list to a formatted string for the prompt
    concepts_text = json.dumps(concepts, indent=2)
    user_prompt = f"Please expand these 3 ad concepts into a detailed raw narrative:\n\n{concepts_text}"
    
    try:
        response = client.models.generate_content(
            model='gemini-1.5-pro',
            contents=user_prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )
        return response.text
    except Exception as e:
        print(f"Error expanding concepts: {e}")
        return ""
