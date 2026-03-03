import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_answer(query, context_items):
    """
    Multimodal answer generation using Gemini.
    Injects image captions before attaching actual images
    for stronger semantic grounding.
    """

    # Limit context to top 2 items to control token usage
    context_items = context_items[:2]

    parts = []

    # 🔹 System instruction
    parts.append(f"""
You are an enterprise multimodal reasoning assistant.

User Question:
{query}

Use ONLY the provided context to answer.
If numeric values are present in images, extract them precisely.
If the answer cannot be determined from context, say so clearly.
""")

    # 🔹 Attach context
    for item in context_items:

        # ---- TEXT CONTEXT ----
        if item["type"] == "text":
            parts.append(f"[TEXT CONTEXT]\n{item['content']}")

        # ---- IMAGE CONTEXT ----
        elif item["type"] == "image":
            try:
                # ✅ Inject caption first (VERY IMPORTANT)
                caption = item.get("description", "")
                if caption:
                    parts.append(f"[IMAGE DESCRIPTION]\n{caption}")

                # ✅ Attach actual image for multimodal reasoning
                image_path = item["content"]
                img = Image.open(image_path)
                parts.append(img)

            except Exception as e:
                # Fallback to caption-only if image fails
                fallback_caption = item.get("description", "")
                if fallback_caption:
                    parts.append(f"[IMAGE DESCRIPTION]\n{fallback_caption}")

        # ---- DOCUMENT CONTEXT (Optional Future Support) ----
        elif item["type"] == "document":
            parts.append(f"[DOCUMENT INFO]\n{item['content']}")

    print("Calling Gemini API...")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=parts,
    )

    return response.text