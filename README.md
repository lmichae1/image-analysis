# AI Media Analyzer

A **Streamlit-based application** that leverages **Azure AI Vision** to analyze images, detect objects, people, tags, and extract text using OCR. Built as a learning project to practice **Azure AI Vision services**.


## Features

- **Image Captioning** – Generates a description of the uploaded image.
- **Object Detection** – Detects objects in the image and displays confidence scores.
- **People Detection** – Detects people, bounding boxes, and confidence levels.
- **Tag Extraction** – Lists relevant tags associated with the image.
- **OCR Text Extraction** – Extracts printed and handwritten text from images.
- **Annotated Image Display** – Visualizes detected objects and people on the uploaded image.

---

## Learnings from Azure AI Vision

This project demonstrates the following Azure AI Vision concepts:

1. **Image Analysis**  
   - Detect tags, objects, people, and captions from images.

2. **OCR (Optical Character Recognition)**  
   - Extract printed and handwritten text from images.

3. **Bounding Box Annotation**  
   - Draw bounding boxes around detected objects and people using PIL.

4. **Confidence Scores**  
   - Understand and display confidence levels for tags, objects, and people.

5. **Streamlit Integration**  
   - Display analysis results in a **user-friendly web interface**.

---

### Prerequisites

- Python 3.9+
- Azure subscription with **Cognitive Services** and **Computer Vision** enabled
- Streamlit (`pip install streamlit`)
- Azure AI Vision SDK (`pip install azure-ai-vision`)

### Setup
1. Clone the repository:
git clone https://github.com/lmichae1/image-analysis.git
cd visionary-ai-analyzer

2. Install dependencies
pip install -r requirements.txt

3. Add your Azure credentials in .env:
AZURE_ENDPOINT=your_azure_endpoint
AZURE_KEY=your_azure_key

4. Run the app:
streamlit run app.py