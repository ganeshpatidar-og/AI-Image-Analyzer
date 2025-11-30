import os
import base64
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv
from PIL import Image         
from io import BytesIO    

# Load environment variables from .env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "x-ai/grok-4.1-fast:free")
OPENROUTER_URL = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
APP_URL = os.getenv("APP_URL", "http://localhost:5000")
APP_TITLE = os.getenv("APP_TITLE", "AI Image Analyzer")

app = Flask(__name__)

def convert_image_to_jpeg(image_bytes):
    """
    Convert any supported image format (PNG, AVIF, HEIC, etc.)
    into JPEG bytes so the AI API can understand it.
    Returns (jpeg_bytes, 'image/jpeg').
    """
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            # Convert modes like RGBA / P to RGB for JPEG
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=90)
            jpeg_bytes = buffer.getvalue()

        return jpeg_bytes, "image/jpeg"
    except Exception as e:
        raise RuntimeError(f"Could not process this image format: {e}")


def call_openrouter_grok(image_bytes, mime_type, task_type):
    """
    Send the image + prompt to OpenRouter (Grok 4.1 Fast) and return the text response.
    """

    # 1. Task-specific prompt
    if task_type == "objects":
        prompt = (
            "You are an image analysis assistant.\n"
            "Describe all important objects in this image and their relationships.\n"
            "Reply in clear bullet points."
        )
    elif task_type == "text":
        prompt = (
            "Extract any readable text from this image, then provide a short summary "
            "of what the text is about."
        )
    elif task_type == "scan":
        prompt = (
            "You are acting like an object scanner in a shopping app.\n"
            "Focus only on the main object in the image and ignore the background as much as possible.\n"
            "Identify the object and give details in this format:\n\n"
            "1) Name of object\n"
            "2) Category/type (e.g., 'electronic gadget', 'kitchen utensil', 'clothing', etc.)\n"
            "3) Visible colors and material\n"
            "4) Typical uses of this object\n"
            "5) 3–5 possible search keywords a user could type to find this object online.\n\n"
            "If you are not sure, still make your best reasonable guess and mention the uncertainty."
        )
    else:  # metadata
        prompt = (
            "Analyze this image and provide:\n"
            "1) A short caption,\n"
            "2) Main objects,\n"
            "3) Dominant colors,\n"
            "4) Overall mood or context."
        )

    # 2. Encode image as base64 data URL
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:{mime_type};base64,{image_b64}"

    # 3. Headers required by OpenRouter
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": APP_URL,   # optional but recommended
        "X-Title": APP_TITLE,      # optional but recommended
    }

    # 4. Payload using OpenAI-style chat.completions schema
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": data_url},
                    },
                ],
            }
        ],
        "max_tokens": 800,
    }

    # 5. Send request
    response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    # 6. Extract text from response
    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        text = f"Model did not return expected content. Raw response:\n{data}"

    return text


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        if "image" not in request.files or request.files["image"].filename == "":
            error = "Please upload an image."
        else:
            img_file = request.files["image"]
            task_type = request.form.get("task_type", "objects")

            try:
                original_bytes = img_file.read()
                converted_bytes, mime_type = convert_image_to_jpeg(original_bytes)

                if not OPENROUTER_API_KEY:
                    raise RuntimeError(
                        "OPENROUTER_API_KEY is not set. Please add it to your .env file."
                    )

                result = call_openrouter_grok(converted_bytes, mime_type, task_type)
            except Exception as e:
                error = f"Error during analysis: {e}"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    # debug=True for development; set to False in production
    app.run(debug=True)
