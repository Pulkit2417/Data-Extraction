import google.generativeai as genai
import PIL.Image
import os
from dotenv import load_dotenv
from pdf2image import convert_from_path


# Load environment variables
load_dotenv()

# Configure Google Generative AI with the API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

prompt = """
There are details of 30 people in the image. I want each person's details in the format I just provided for you:
1. Lina Shaktikumar Cavan
   Husband's Name: Shaktikumar Chavan
   Age: 37
   Gender: Female
   House No: None
   EPIC No.: TXK6940811
"""
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

pdf_file = 'Sample Problem.pdf'
images = convert_from_path(pdf_file)
for i, img in enumerate(images):
    response = model.generate_content([prompt, img])
    print(response.text)