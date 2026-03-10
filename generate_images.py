"""Generate blog post images using Gemini Pro via AWS Secrets Manager."""
import asyncio
import base64
import json
import logging
import os
import sys

import boto3
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"
GEMINI_MODEL = "gemini-3-pro-image-preview"
MAX_RETRIES = 3
RETRY_STATUS_CODES = {429, 500, 503}


def load_gemini_api_key() -> str:
    """Load Gemini API key: env var first, then AWS Secrets Manager (temp profile)."""
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        logger.info("Using GEMINI_API_KEY from environment")
        return key

    try:
        session = boto3.Session(profile_name="temp")
        client = session.client("secretsmanager", region_name="us-west-2")
        resp = client.get_secret_value(SecretId="stylix/gemini")
        data = json.loads(resp["SecretString"])
        key = data.get("api-key", "")
        if key:
            logger.info("Loaded Gemini API key from Secrets Manager (temp profile)")
            return key
    except Exception as e:
        logger.warning(f"Secrets Manager failed: {e}")

    raise RuntimeError("No Gemini API key available")


async def generate_image(api_key: str, prompt: str, output_path: str) -> str:
    """Generate an image using Gemini Pro and save to disk."""
    url = f"{GEMINI_API_BASE}/models/{GEMINI_MODEL}:generateContent"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        },
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }

    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(url, json=payload, headers=headers)

                if response.status_code in RETRY_STATUS_CODES and attempt < MAX_RETRIES - 1:
                    wait = 2 ** attempt
                    logger.warning(f"Status {response.status_code}, retrying in {wait}s...")
                    await asyncio.sleep(wait)
                    continue

                response.raise_for_status()

            data = response.json()
            for candidate in data.get("candidates", []):
                for part in candidate.get("content", {}).get("parts", []):
                    if "inlineData" in part:
                        inline = part["inlineData"]
                        image_data = inline["data"]
                        image_bytes = base64.b64decode(image_data)

                        with open(output_path, "wb") as f:
                            f.write(image_bytes)

                        logger.info(f"Saved image to {output_path} ({len(image_bytes)} bytes)")
                        return output_path

            logger.warning("No image in Gemini response")
            last_error = RuntimeError("No image in response")

        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                wait = 2 ** attempt
                logger.warning(f"Error on attempt {attempt + 1}, retrying in {wait}s: {e}")
                await asyncio.sleep(wait)
                continue
            break

    raise last_error or RuntimeError("Image generation failed")


async def main():
    api_key = load_gemini_api_key()
    output_dir = "static/images/build-the-factory"

    images = [
        {
            "filename": "craftsman-vs-factory.png",
            "prompt": (
                "Create a wide cinematic illustration in a modern flat style with bold colors. "
                "Split composition: on the left, a lone developer hunched over a laptop writing code line by line "
                "in a dim workshop with hand tools on the wall — representing the craftsman approach. "
                "On the right, the same developer standing confidently at a control panel overlooking "
                "an automated factory floor with robotic arms assembling software components on a conveyor belt — "
                "representing the factory builder approach. "
                "A glowing dividing line separates the two halves. "
                "No text. Clean, editorial, tech blog style. 16:9 aspect ratio."
            ),
        },
        {
            "filename": "iteration-loop.png",
            "prompt": (
                "Create a wide cinematic illustration in a modern flat style with bold colors. "
                "Show a circular feedback loop floating in space: five connected nodes forming a cycle — "
                "Define (blueprint icon) → Run (play button) → Observe (magnifying glass) → "
                "Refine (wrench/gear) → Repeat (circular arrow back to Define). "
                "In the center of the loop, a glowing AI chip or brain symbol. "
                "Each iteration of the loop gets slightly brighter and more refined, "
                "suggesting improvement over time. "
                "Dark background with vibrant accent colors. "
                "No text. Clean, editorial, tech blog style. 16:9 aspect ratio."
            ),
        },
        {
            "filename": "leverage-multiplier.png",
            "prompt": (
                "Create a wide cinematic illustration in a modern flat style with bold colors. "
                "Show two contrasting paths diverging from a starting point: "
                "The top path shows a single developer manually producing small boxes (outputs) one at a time, "
                "a slow linear progression with few results. "
                "The bottom path shows a developer building a machine in the first segment (investing upfront), "
                "then the machine mass-producing hundreds of boxes automatically in the second segment — "
                "an exponential explosion of output. "
                "A timeline arrow runs along the bottom showing the crossover point "
                "where the system builder overtakes the manual coder. "
                "No text. Clean, editorial, tech blog style. 16:9 aspect ratio."
            ),
        },
    ]

    tasks = []
    for img in images:
        path = os.path.join(output_dir, img["filename"])
        tasks.append(generate_image(api_key, img["prompt"], path))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for img, result in zip(images, results):
        if isinstance(result, Exception):
            logger.error(f"Failed to generate {img['filename']}: {result}")
        else:
            logger.info(f"Success: {result}")


if __name__ == "__main__":
    asyncio.run(main())
