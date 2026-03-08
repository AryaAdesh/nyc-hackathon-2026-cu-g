class DataInfuser:
    def __init__(self, model):
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
        
        # This call would use Gemini's 'response_mime_type': 'application/json'
        # with the DataInfuserOutput schema provided above.
        response = await self.model.generate_content(
            f"{system_instruction}\n\nInput Narratives: {raw_narratives}"
        )
        return DataInfuserOutput.model_validate_json(response.text)