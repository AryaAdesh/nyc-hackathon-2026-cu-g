from .infuser_schema import DataInfuserOutput
from google.genai import types

class DataInfuser:
    def __init__(self, model):
        # We assume main.py passes client.aio.models for async operations
        self.model = model

    async def infuse_data(self, raw_narratives: str) -> DataInfuserOutput:
        system_instruction = """
        You are a Technical Data Infuser. 
        Your task is to extract technical parameters from 3 story ideas.
        RULES:
        1. No conversational filler. 
        2. 'veo_prompt' must focus on movement and temporal changes.
        3. 'nano_banana_prompt' must focus on textures and lighting.
        4. You MUST follow the provided JSON schema exactly.
        5. If a narrative is vague, you must choose the most fitting technical parameter (e.g., 'fast' becomes 'high' motion_intensity).
        """
        
        response = await self.model.generate_content(
            model='gemini-2.0-flash-001',
            contents=f"Input Narratives:\n{raw_narratives}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=DataInfuserOutput,
                temperature=0.2,
            )
        )
        return DataInfuserOutput.model_validate_json(response.text)