"""Generate blog post images using Gemini Pro via AWS Secrets Manager."""
import asyncio
import base64
import json
import logging
import os

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


# --- Image definitions per post ---

POSTS = {
    "build-the-factory": [
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
    ],
    "tdd-for-agentic-workflows": [
        {
            "filename": "agentic-codebase.png",
            "prompt": (
                "A simple, hand-drawn style whiteboard sketch on a plain white background. "
                "Four boxes arranged in a square: 'Tests' (top-left, with a checkmark), "
                "'Prompts' (top-right, with a chat bubble), 'Tools' (bottom-left, with a wrench), "
                "'Orchestrator' (bottom-right, with arrows connecting to the other three). "
                "Drawn with a black marker, slightly imperfect lines, like a real whiteboard diagram. "
                "Minimal, no decoration, no gradients, no color except maybe a single red circle "
                "around the word 'Tests' to emphasize it. "
                "The kind of sketch a senior engineer draws in a meeting to explain the whole system in 30 seconds. "
                "No text labels other than the four box names. 16:9 aspect ratio."
            ),
        },
        {
            "filename": "ground-truth-loop.png",
            "prompt": (
                "A simple, hand-drawn style diagram on a plain white background. "
                "A circular loop with five steps drawn as rough boxes connected by arrows: "
                "Run → Measure → Analyze Failures → Refine → back to Run. "
                "In the center of the loop, a simple table icon representing a dataset "
                "with rows of checkmarks and X marks (ground truth). "
                "Below the loop, a simple bar chart showing precision and recall bars "
                "getting taller with each iteration, approaching 100%. "
                "Black marker on white, slightly messy handwriting style, "
                "like a sketch on paper during a brainstorming session. "
                "No decoration, no gradients. 16:9 aspect ratio."
            ),
        },
        {
            "filename": "tests-vs-code.png",
            "prompt": (
                "A simple, hand-drawn style comparison sketch on a plain white background. "
                "Left side: a tall, messy stack of papers/documents labeled with tiny scribbles, "
                "representing a traditional codebase with layers upon layers (frameworks, services, ORM, glue code). "
                "Right side: a short, clean stack of just four thin papers, "
                "representing the agentic codebase (tests, prompts, tools, config). "
                "A simple bracket or arrow pointing to the right stack. "
                "Black marker on white, rough sketch style, like a napkin drawing at a coffee shop. "
                "No color except the right stack might have a slight green highlight. "
                "No fancy rendering. Authentic and minimal. 16:9 aspect ratio."
            ),
        },
    ],
    "spec-driven-development": [
        {
            "filename": "ottoman-court.png",
            "prompt": (
                "Create a wide cinematic illustration blending Ottoman Empire aesthetics with modern technology. "
                "An ornate Ottoman council chamber (Divan) with arched doorways, mosaic tiles, and warm golden light — "
                "but instead of human officials, the seats around the council table are occupied by "
                "glowing AI avatars / holographic figures, each with a distinct role icon floating above them: "
                "a crown (Grand Vizier/orchestrator), a quill (scribe/planner), a compass (architect), "
                "a hammer (craftsman/builder), a magnifying glass (inspector/reviewer). "
                "In the center of the table, floating YAML code scrolls glow like ancient decrees. "
                "No text. Rich, editorial, tech blog style with Ottoman color palette (gold, deep blue, crimson). 16:9 aspect ratio."
            ),
        },
        {
            "filename": "contract-validation.png",
            "prompt": (
                "Create a wide cinematic illustration in a modern flat style with bold colors. "
                "Show a conveyor belt carrying glowing document cards (representing agent outputs). "
                "At a checkpoint gate, a stern robotic inspector with a magnifying glass examines each card "
                "against a floating YAML schema blueprint. Cards that pass get a green checkmark stamp "
                "and continue forward. Cards that fail get a red X and are sent back on a return conveyor. "
                "The scene conveys automated quality control and contract validation. "
                "No text. Clean, editorial, tech blog style. 16:9 aspect ratio."
            ),
        },
        {
            "filename": "vibes-vs-specs.png",
            "prompt": (
                "Create a wide cinematic illustration in a modern flat style with bold colors. "
                "Split composition: on the left side, chaos — multiple AI agents running in different directions, "
                "papers flying everywhere, confused speech bubbles, tangled connections between them, "
                "a sign that is blurry and vague (representing vibes-based development). "
                "On the right side, order — the same agents arranged in a clean pipeline, "
                "connected by glowing contract documents, each agent handing validated output to the next, "
                "a clear flow from start to finish (representing spec-driven development). "
                "A glowing dividing line separates the two halves. "
                "No text. Clean, editorial, tech blog style. 16:9 aspect ratio."
            ),
        },
    ],
}


async def main():
    import sys

    api_key = load_gemini_api_key()

    # Allow specifying which post to generate for
    post_slug = sys.argv[1] if len(sys.argv) > 1 else None

    if post_slug and post_slug not in POSTS:
        print(f"Unknown post: {post_slug}")
        print(f"Available: {', '.join(POSTS.keys())}")
        sys.exit(1)

    posts_to_generate = {post_slug: POSTS[post_slug]} if post_slug else POSTS

    for slug, images in posts_to_generate.items():
        output_dir = f"static/images/{slug}"
        os.makedirs(output_dir, exist_ok=True)

        # Skip if all images already exist
        missing = [img for img in images if not os.path.exists(os.path.join(output_dir, img["filename"]))]
        if not missing:
            logger.info(f"All images for '{slug}' already exist, skipping")
            continue

        logger.info(f"Generating {len(missing)} images for '{slug}'...")
        tasks = []
        for img in missing:
            path = os.path.join(output_dir, img["filename"])
            tasks.append(generate_image(api_key, img["prompt"], path))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for img, result in zip(missing, results):
            if isinstance(result, Exception):
                logger.error(f"Failed to generate {img['filename']}: {result}")
            else:
                logger.info(f"Success: {result}")


if __name__ == "__main__":
    asyncio.run(main())
