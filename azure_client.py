"""
Demo AI Media Analyzer
Copyright (c) 2025 lmichae1

This software is licensed under the MIT License.
See the LICENSE file in the repository root for details.
"""

import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from PIL import Image, ImageDraw
from dotenv import load_dotenv

load_dotenv()

# Load Azure credentials from Streamlit secrets or environment variables
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_KEY")

# Initialize Azure AI Vision client
client = ImageAnalysisClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_KEY)
)

# -------------------
# Analyze Image
# -------------------
def analyze_image(image_file):
    """Analyze image for tags, objects, people, and caption."""
    image_bytes = image_file.read()

    result = client.analyze(
        image_data=image_bytes,
        visual_features=[
            VisualFeatures.TAGS,
            VisualFeatures.OBJECTS,
            VisualFeatures.PEOPLE,
            VisualFeatures.CAPTION
        ]
    )

    # --- Process tags ---
    tags_list = []
    if result.tags and hasattr(result.tags, "list"):
        for tag in result.tags.list:
            tags_list.append({
                "name": tag.name,
                "confidence": round(tag.confidence, 2)
            })

    # --- Process objects ---
    objects_list = []
    if result.objects and hasattr(result.objects, "list"):
        for obj in result.objects.list:
            obj_name = obj.tags[0].name if obj.tags else "Unknown"
            obj_conf = round(obj.tags[0].confidence, 2) if obj.tags else None
            objects_list.append({
                "bounding_box": obj.bounding_box,
                "name": obj_name,
                "confidence": obj_conf
            })

    # --- Process people ---
    people_list = []
    if result.people and hasattr(result.people, "list"):
        for person in result.people.list:
            if person.confidence > 0.2:
                people_list.append({
                    "bounding_box": person.bounding_box,
                    "confidence": round(person.confidence, 2)
                })

    # --- Process caption ---
    caption_dict = None
    if result.caption:
        caption_dict = {
            "text": result.caption.text,
            "confidence": round(result.caption.confidence, 2)
        }

    return {
        "tags": tags_list,
        "objects": objects_list,
        "people": people_list,
        "caption": caption_dict
    }

# -------------------
# Extract OCR text
# -------------------
def extract_text(image_file):
    image_bytes = image_file.read()

    result = client.analyze(
        image_data=image_bytes,
        visual_features=[VisualFeatures.READ]
    )

    text_output = ""
    if result.read is not None:
        for block in result.read.blocks:
            for line in block.lines:
                text_output += line.text + "\n"

    return text_output.strip()

# -------------------
# Annotate objects
# -------------------
def show_objects(image: Image.Image, objects_list):
    draw = ImageDraw.Draw(image)
    color = "cyan"

    for obj in objects_list:
        bbox = obj["bounding_box"]
        x, y, w, h = bbox.x, bbox.y, bbox.width, bbox.height
        draw.rectangle([(x, y), (x + w, y + h)], outline=color, width=3)
        if obj["name"]:
            draw.text((x, y - 10), f"{obj['name']} ({obj['confidence']})", fill=color)

    return image

# -------------------
# Annotate people
# -------------------
def show_people(image: Image.Image, people_list):
    draw = ImageDraw.Draw(image)
    color = "red"

    for person in people_list:
        bbox = person["bounding_box"]
        x, y, w, h = bbox.x, bbox.y, bbox.width, bbox.height
        draw.rectangle([(x, y), (x + w, y + h)], outline=color, width=3)
        draw.text((x, y - 10), f"{person['confidence']}", fill=color)

    return image
