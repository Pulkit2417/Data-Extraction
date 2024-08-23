import google.generativeai as genai
import os
import pandas as pd
from dotenv import load_dotenv
from pdf2image import convert_from_path
import ast

# Load environment variables
load_dotenv()

# Configure Google Generative AI with the API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Define the prompt for Generative AI to return Python dictionaries
prompt = """
There are details of 30 people in the image, however some of them marked as deleted.
I want each person's details (excluding deleted) in the format of a Python dictionary:
{
    "Part S.No": "1",
    "Voter Full Name": "LINA SHAKTIKUMAR CHAVAN",
    "Relative's Name": "SHAKTIKUMAR CHAVAN",
    "Relation Type": "HSBN",
    "Age": "37",
    "Gender": "F",
    "House No": "",
    "EPIC No": "TXK6940811"
}
Use FTHR, HSBN, OTHR, as relation type for Father, Husband and Other respectively.
Use M and F as gender for male and female respectively.
"""

# Set up the Generative AI model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Convert PDF to images
pdf_file = 'Sample Problem.pdf'
images = convert_from_path(pdf_file)

# Process each image and extract information
all_extracted_details = []

for i, img in enumerate(images):
    try:
        response = model.generate_content([prompt, img])
        if 'error' in response or not response.text:
            print(f"Error in processing image {i+1}: {response.get('error', 'No response text')}")
            continue
        
        # Safe evaluation of the response
        extracted_details = ast.literal_eval(response.text.replace("```", '').replace("python", '').strip())
        all_extracted_details.extend(extracted_details)
        
    except Exception as e:
        print(f"Exception occurred while processing image {i+1}: {str(e)}")
        continue

# Convert the list of dictionaries to a DataFrame and save to Excel
df = pd.DataFrame(all_extracted_details)

# Ensure all column names are in uppercase
df.columns = df.columns.str.upper()

# Save the DataFrame to Excel
output_file = 'final_output.xlsx'
df.to_excel(output_file, index=False)

print(f"Details have been extracted and saved to {output_file}")
