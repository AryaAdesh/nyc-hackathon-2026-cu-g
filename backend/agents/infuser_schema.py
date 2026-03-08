from pydantic import BaseModel, Field
from typing import Literal, List

class VideoSpecs(BaseModel):
    motion_intensity: Literal["low", "medium", "high"] = Field(..., description="The speed of movement in Veo")
    camera_angle: Literal["drone", "cinematic-close-up", "wide-pan", "static"]
    audio_cue: str = Field(..., max_length=100, description="Native audio for Veo")

class ImageSpecs(BaseModel):
    aspect_ratio: Literal["16:9", "1:1", "9:16"]
    art_style: Literal["photorealistic", "digital-art", "oil-painting", "cyberpunk-neon"]
    lighting: str = Field(..., description="Specific lighting instructions (e.g., 'Golden Hour')")

class InfusedStory(BaseModel):
    title: str
    veo_prompt: str
    veo_specs: VideoSpecs
    nano_banana_prompt: str
    nano_banana_specs: ImageSpecs
    live_instructions: str = Field(..., description="Persona for Gemini Live")

class DataInfuserOutput(BaseModel):
    # This enforces that we always get exactly 3 restricted outputs
    story_packages: List[InfusedStory] = Field(..., min_items=3, max_items=3)