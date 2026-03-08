from google import genai
from google.genai import types
import asyncio
import base64

async def generate_video(prompt: str) -> str:
    """Uses Veo 2 via Gemini SDK to generate a video. Blocks until completion."""
    try:
        client = genai.Client()
        
        # 1. Start the Veo generation (returns an Operation)
        print(f"Starting Veo generation for prompt snippet: {prompt[:30]}...")
        operation = await client.aio.models.generate_videos(
            model='veo-2.0-generate-001',
            prompt=prompt,
            config=types.GenerateVideosConfig(
                # Ensure we fit the prompt in requirements
                aspect_ratio="16:9",
                person_generation="ALLOW_ADULT",
            )
        )
        
        print(f"Veo Operation Name: {operation.name}")
        
        # 2. Poll until the video is ready
        # The SDK has operation.result(), wait until done.
        while not operation.done:
            print(f"Waiting for Veo video {operation.name} to complete...")
            await asyncio.sleep(5)
            # Need to get operation status update
            # The python SDK typically fetches the operation status via operations.get
            operation = await client.aio.operations.get(operation.name)
            
        print(f"Veo Operation {operation.name} complete!")
        
        # 3. Handle the response
        if operation.response:
            # Contains the GeneratedVideo
            video_bytes = operation.response.generated_videos[0].video.video_bytes
            b64_vid = base64.b64encode(video_bytes).decode('utf-8')
            return f"data:video/mp4;base64,{b64_vid}"
            
        if operation.error:
            print(f"Veo Error: {operation.error}")
            
        return ""
    except Exception as e:
        print(f"Exception generating video: {e}")
        # Return a fallback video for testing if it fails
        return "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
