from google import genai
from google.genai import types

async def generate_image(prompt: str) -> str:
    """Uses Imagen 3 via Gemini SDK to generate an image."""
    try:
        client = genai.Client() # Assumes GEMINI_API_KEY
        
        # In a real app we'd save the image to GCS or disk and return the URL.
        # For the hackathon, we can generate a base64 string or save locally.
        # Let's hit the API. Google Genai SDK for image generation:
        result = await client.aio.models.generate_images(
            model='imagen-3.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
                output_mime_type="image/jpeg",
            )
        )
        
        # Result contains a list of GeneratedImage objects.
        # We can extract the image bytes. To serve it to the frontend easily without a bucket,
        # we can encode it as a base64 data URI.
        import base64
        if result.generated_images:
            image_bytes = result.generated_images[0].image.image_bytes
            b64_img = base64.b64encode(image_bytes).decode('utf-8')
            return f"data:image/jpeg;base64,{b64_img}"
            
        return ""
    except Exception as e:
        print(f"Error generating image: {e}")
        # Return a fallback gradient or placeholder for testing if it fails
        return "https://placehold.co/1920x1080/000000/FFFFFF/png?text=Image+Failed"
