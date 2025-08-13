"""
Demo AI Media Analyzer
Copyright (c) 2025 lmichae1

This software is licensed under the MIT License.
See the LICENSE file in the repository root for details.
"""

import streamlit as st
from azure_client import analyze_image, extract_text, show_objects, show_people
from PIL import Image

st.set_page_config(page_title="AI Media Analyzer", layout="wide")
st.title("👁️ Visionary: AI-powered Media Analyzer")
st.write("Upload an image to analyze objects, tags, people, and extract text using Azure AI Vision.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image once
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Reset pointer and analyze
    uploaded_file.seek(0)
    analysis_result = analyze_image(uploaded_file)

    # -------------------
    # Image Caption
    # -------------------
    st.subheader("📌 Image Description")
    caption = analysis_result.get("caption")
    if caption:
        st.write(f"**Caption:** {caption['text']} (Confidence: {caption['confidence']:.2f})")
    else:
        st.info("No caption detected.")

    # -------------------
    # Tags
    # -------------------
    st.subheader("🏷️ Tags")
    tags = analysis_result.get("tags", [])
    if tags:
        for tag in tags:
            st.write(f"• **{tag['name']}** ({tag['confidence'] * 100:.2f}%)")
    else:
        st.info("No tags detected.")

    # -------------------
    # Objects
    # -------------------
    st.subheader("📦 Detected Objects")
    objects = analysis_result.get("objects", [])
    if objects:
        for obj in objects:
            name = obj["name"]
            conf = obj["confidence"] * 100 if obj["confidence"] else None
            st.write(f"• **{name}** ({conf:.2f}%)" if conf else f"• {name}")
        annotated_objects = show_objects(image.copy(), objects)
        st.image(annotated_objects, caption="Detected Objects", use_container_width=True)
    else:
        st.info("No objects detected.")

    # -------------------
    # People
    # -------------------
    st.subheader("🧍 People in Image")
    people = analysis_result.get("people", [])
    if people:
        for person in people:
            bbox = person["bounding_box"]
            conf = person["confidence"] * 100
            st.write(f"• Bounding box: {bbox}, Confidence: {conf:.2f}%")
        annotated_people = show_people(image.copy(), people)
        st.image(annotated_people, caption="Detected People", use_container_width=True)
    else:
        st.info("No people detected.")

    # -------------------
    # OCR
    # -------------------
    uploaded_file.seek(0)
    st.subheader("🔍 Extracted Text (OCR)")
    text_result = extract_text(uploaded_file)
    st.text(text_result if text_result else "No text found.")
