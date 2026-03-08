import requests
import json
import time

BASE_URL = "http://localhost:8000"

def run_test():
    prompt = "A sleek, next-generation electric sports car designed for Mars."
    print(f"--- 1. Generating Concepts for: '{prompt}' ---")
    start = time.time()
    try:
        res = requests.post(f"{BASE_URL}/api/generate-concepts", json={"prompt": prompt})
        concepts = res.json()
    except Exception as e:
        print("API NOT RUNNING OR FAILED", e)
        return
        
    print(f"Elapsed: {time.time() - start:.2f}s")
    print(json.dumps(concepts, indent=2))
    print()

    print("--- 2. Expanding Concepts ---")
    start = time.time()
    res = requests.post(f"{BASE_URL}/api/expand-concepts", json={"concepts": concepts})
    raw_narrative = res.json()["raw_narrative"]
    print(f"Elapsed: {time.time() - start:.2f}s")
    print(raw_narrative[:500] + "... [truncated]")
    print()

    print("--- 3. Infusing Data ---")
    start = time.time()
    res = requests.post(f"{BASE_URL}/api/infuse-data", json={"raw_narrative": raw_narrative})
    infused = res.json()
    print(f"Elapsed: {time.time() - start:.2f}s")
    print(json.dumps(infused, indent=2))
    print()

    print("--- 4. Generating Media (THIS WILL TAKE TIME) ---")
    # For testing, just take the first one
    body = {"infused_stories": [infused["story_packages"][0]]}
    start = time.time()
    res = requests.post(f"{BASE_URL}/api/generate-media", json=body)
    final_output = res.json()
    print(f"Elapsed: {time.time() - start:.2f}s")
    
    story = final_output.get("stories", [{}])[0]
    img = story.get("imageUrl", "")[:50]
    vid = story.get("videoUrl", "")[:50]
    print(f"Image generated: {img}...")
    print(f"Video generated: {vid}...")
    print("TEST COMPLETE!")

if __name__ == "__main__":
    run_test()
